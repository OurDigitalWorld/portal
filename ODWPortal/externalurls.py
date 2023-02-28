from urllib import parse
from lxml import etree
from ODWPortal.utilities import get_media_label
from ODWPortal.querySolr import solr_query
from ODWPortal.parts import get_solr
from Portal.settings import XSL_PATH, SOLR_URL

# from Portal.customlog import log_request

solr = '%ssearch/query/?wt=json' % SOLR_URL
solr_xml = '%ssearch/query/?wt=xml' % SOLR_URL


# TODO exactly the same code as get_parts ... reconcile


def get_facet(f, search_set):
    url = ('%s&q=%s'
           '&rows=0'
           '&facet=true'
           '&facet.field=%s'
           '&facet.zeros=false&facet.limit=-1'
           % (solr, search_set, f))
    return get_solr(url, 'json')


def list_facet(solr_field, portal_field, result_path, display, site_language, search_set):
    solr_response = get_facet(solr_field, search_set)
    facet_list = ''
    if isinstance(solr_response, dict):
        facets = solr_response['facet_counts']['facet_fields'][solr_field]
        labels = facets[::2]
        counts = facets[1::2]
        if display == 'option':
            facet_list = option_list(labels, counts)
        elif display == 'radio':
            facet_list = html_list('radio', labels, counts, portal_field, result_path, site_language)
        elif display == 'checkbox':
            facet_list = html_list('checkbox', labels, counts, portal_field, result_path, site_language)
        elif display == 'plain_list':
            facet_list = plain_list(labels, counts, portal_field, result_path, site_language)
        else:
            facet_list = ''
    return facet_list


def option_list(labels, counts):
    html = ''
    for label, count in zip(labels, counts):
        if len(label) > 0:
            html += '<option value="%s">%s (%s)</option> \n' % (label, label, count)
    return html


def html_list(display, labels, counts, portal_field, result_path, site_language):
    html = ''
    for label, count in zip(labels, counts):
        if portal_field == 'mt':
            original_label = label
            label = get_media_label(label.title(), site_language)
        else:
            original_label = label
            label = label
        query = parse.quote_plus(label)
        if label:
            html += (('<li>'
                      '<input id="%s_%s" '
                      'type="%s" '
                      'name="%s" '
                      'value="%s" /> '
                      '<label for="%s_%s">'
                      '<a href="/%s?%s=%s">'
                      '%s'
                      '</a>'
                      '</label> (%s)'
                      '</li>')
                     % (portal_field, ''.join(label.split(' ')),
                        display,
                        portal_field, original_label,
                        portal_field, ''.join(label.split(' ')),
                        result_path, portal_field, query,
                        label, count))
    return html


def plain_list(labels, counts, portal_field, result_path, site_language):
    html = ''
    for label, count in zip(labels, counts):
        if portal_field == 'mt':
            label = get_media_label(label.title(), site_language)
        else:
            label = label
        query = parse.quote_plus(label)
        if label:
            html += '<li><a href="/%s?%s=%s">%s</a> (%s)</li>' \
                     % (result_path, portal_field, query, label, count)
    return html


def media_facet(request, result_path, search_set):
    nvps = request
    if 'mt' in nvps:
        media_type = nvps.get('mt')
        query = parse.quote_plus(media_type)
        url = ('%s&q=(type:%s+AND+%s)'
               '&rows=0'
               '&facet=true'
               '&facet.field=itemType'
               '&facet.zeros=false'
               '&facet.limit=-1'
               % (solr, query, search_set))
        solr_response = get_solr(url, 'json')
        if isinstance(solr_response, dict):
            facets = solr_response['facet_counts']['facet_fields']['itemType']
            labels = facets[::2]
            counts = facets[1::2]
            html = ''
            for label, count in zip(labels, counts):
                item_type = parse.quote_plus(label)
                html += ('<li>'
                         '<input type="checkbox" '
                         'id="%s" '
                         'name="itype" '
                         'value="%s" /> '
                         '<a href="/%s?itype=%s&amp;mt=%s">'
                         '<label for="%s">%s</label>'
                         '</a>'
                         ' (%s)</li>'
                         % (''.join(label.split(' ')), label, result_path,
                            item_type, media_type, ''.join(label.split(' ')),
                            label, count))
            return html
    else:
        return ''


def query_solr_url(request, output_format, xml_type, search_set):
    """
    generate the appropriate URLs for requests
    execute the searches against solr, or external datasets
    """
    query_str, query_dict = solr_query(request, xml_type, search_set)
    if output_format == 'xml':
        url = solr_xml + query_str
    else:
        url = solr + query_str
    # log_request('url (enternalurls.151)', url)
    solr_result = get_solr(url, output_format)
    return solr_result, query_dict


def get_docs(request, search_set):
    num_found = 0
    rows = 0
    docs = {}
    facets = {}
    solr_response, query_dict = query_solr_url(request, 'json', 'html', search_set)
    if isinstance(solr_response, dict):
        # log_request('solr_response (enternalurls.178)', solr_response)
        rows = solr_response['responseHeader']['params']['rows']
        num_found = solr_response['response']['numFound']
        docs = solr_response['response']['docs']
        facets = solr_response['facet_counts']['facet_fields']
    if "p" in request:
        page_num = str(request.__getitem__('p'))
    else:
        page_num = "1"
    return solr_response, num_found, rows, page_num, docs, facets, query_dict


def get_xml(request, xml_type, search_set):
    """
    take request and transform into appropriate xml package.
    Supports DC, MODS, RDF and SOLR.
    """
    solr_response_list = query_solr_url(request, 'xml', xml_type, search_set)
    # print('solr_response_list: ', solr_response_list)
    response_doc = solr_response_list[0]
    str_response_doc = response_doc.decode('utf-8')
    str_response_doc = str_response_doc.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '')
    # print('str_response_doc: ', str_response_doc)
    if xml_type != "solr":
        xml_doc = etree.XML(str_response_doc)
        # print xmlDoc
        xsl_file = '%s%s.xsl' % (XSL_PATH, xml_type)
        style_doc = etree.parse(xsl_file)
        # print styledoc
        style = etree.XSLT(style_doc)
        xml_transformed = style(xml_doc)
    else:
        xml_transformed = str_response_doc
    return xml_transformed


def get_json(request, search_set):
    solr_response, query_dict = query_solr_url(request, 'json', 'html', search_set)
    return solr_response


def get_count(request, search_set):
    query_str, query_dict = solr_query(request, 'count', search_set)
    count = '0'
    url = solr + query_str
    solr_result = get_solr(url, 'json')
    if isinstance(solr_result, dict):
        count = solr_result['response']['numFound']
    return count
