import urllib
import json
from lxml import etree
from django.utils.http import urlquote
from ODWPortal.utilities import get_media_label
from ODWPortal.querySolr import solr_query
from Portal.settings import XSL_PATH, SOLR_URL

solr = '%ssearch/select/?wt=json' % SOLR_URL
solr_xml = '%ssearch/select/?' % SOLR_URL


#TODO exactly the same code as get_parts ... reconcile
def get_solr(url, output_format):
    try:
        conn = urllib.request.urlopen(url)
        if output_format == "xml":
            rdata = []
            chunk = 'xx'
            while chunk:
                chunk = conn.read()
                if chunk:
                    rdata.append(chunk)
            str1 = rdata
        else:
            str_response = conn.readall().decode('utf-8')
            str1 = json.loads(str_response)
        conn.close()
    except IOError:
        #print 'Cannot open <strong class="highlight">URL</strong> %s for reading' % url
        str1 = 'error!'
    if isinstance(str1, list):
        return_value = str1[0]
    else:
        return_value = str1
    return return_value


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
        else:
            facet_list = ''
    return facet_list


def option_list(labels, counts):
    html = ''
    for l, c in zip(labels, counts):
        if len(l) > 0:
            html += '<option value="%s">%s (%s)</option> \n' % (l, l, c)
    return html


def html_list(display, labels, counts, portal_field, result_path, site_language):
    html = ''
    for l, c in zip(labels, counts):
        if portal_field == 'mt':
            label = get_media_label(l.title(), site_language)
        else:
            label = l
            #asdfl;kj = ur
        query = urlquote(l)
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
                      % (portal_field, ''.join(l.split(' ')),
                         display,
                         portal_field, l,
                         portal_field, ''.join(l.split(' ')),
                         result_path, portal_field, query,
                         label, c))
    return html


def media_facet(request, result_path, search_set):
    nvps = request
    if 'mt' in nvps:
        media_type = nvps.get('mt')
        query = urlquote(media_type)
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
            for l, c in zip(labels, counts):
                item_type = urlquote(l)
                html += ('<li>'
                         '<input type="checkbox" '
                         'id="%s" '
                         'name="itype" '
                         'value="%s" /> '
                         '<a href="/%s?itype=%s&amp;mt=%s">'
                         '<label for="%s">%s</label>'
                         '</a>'
                         ' (%s)</li>'
                         % ( ''.join(l.split(' ')), l, result_path, item_type, media_type, ''.join(l.split(' ')), l, c))
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
    solr_result = get_solr(url, output_format)
    return solr_result, query_dict


def get_kml_count(request, search_set):
    kml_query, query_dict = solr_query(request, 'kml', search_set)
    if kml_query:
        url = solr + kml_query
        kml_response = get_solr(url, 'json')
        if isinstance(kml_response, dict):
            kml_count = int(kml_response['response']['numFound'])
        else:
            kml_count = 0
    else:
        kml_count = 0
    return kml_count


def get_docs(request, search_set):
    num_found = 0
    rows = 0
    docs = {}
    facets = {}
    solr_response, query_dict = query_solr_url(request, 'json', 'html', search_set)
    if isinstance(solr_response, dict):
        rows = solr_response['responseHeader']['params']['rows']
        num_found = solr_response['response']['numFound']
        docs = solr_response['response']['docs']
        facets = solr_response['facet_counts']['facet_fields']
    if "p" in request:
        page_num = str(request.__getitem__('p'))
    else:
        page_num = "1"
    return solr_response, num_found, rows, page_num, docs, facets, query_dict


# TODO:  consider dropping this function ... results.xml output
def get_html(request, querystring, lang, search_set):
    solr_response_list = query_solr_url(request, 'xml', 'stuff', search_set)
    response_doc = solr_response_list[0]
    #print 'passing through XML land'
    xml_doc = etree.parse(response_doc)
    #print lang
    if lang == 'fr':
        xsl_file = '%ssearch_result_fr.xsl' % XSL_PATH
    else:
        xsl_file = '%ssearch_result_min.xsl' % XSL_PATH
    #print xslFile    
    styledoc = etree.parse(xsl_file)
    #print styledoc
    style = etree.XSLT(styledoc)
    qs = "'%s'" % querystring
    param_page = etree.XSLT.strparam("1")
    param_unparsed_query = etree.XSLT.strparam(qs)
    xml_transformed = style(xml_doc, page=param_page, unparsedQuery=param_unparsed_query)
    return xml_transformed


def get_xml(request, xml_type, search_set):
    """
    take request and transform into appropriate xml package.
    Supports DC, MODS, RDF, KML and SOLR.
    """
    solr_response_list = query_solr_url(request, 'xml', xml_type, search_set)
    #print('solrResponseList: ', solrResponseList)
    response_doc = solr_response_list[0]
    str_response_doc = response_doc.decode('utf-8')
    str_response_doc = str_response_doc.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '')
    #print('str_response_doc: ', str_response_doc)
    if xml_type != "solr":
        xml_doc = etree.XML(str_response_doc)
        #print xmlDoc
        xsl_file = '%s%s.xsl' % (XSL_PATH, xml_type)
        style_doc = etree.parse(xsl_file)
        #print styledoc
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


def get_pref_collation(suggestions):
    """
    solr does not order the alternate spelling suggestions by frequency of occurrence
     so we need to loop through looking for the most frequent
    """
    top_hits = 0
    pref_collation = ''
    suggestion_dict1 = suggestions[1]
    if isinstance(suggestion_dict1, dict):
        if 'suggestion' in suggestion_dict1.keys():
            suggestion_list2 = suggestion_dict1.get('suggestion')
            for item in suggestion_list2:
                suggestion_dict2 = item
                hits = int(suggestion_dict2.get('freq'))
                collation = suggestion_dict2.get('word')
                #print(collation,": ", hits)
                if hits > top_hits:
                    top_hits = hits
                    pref_collation = collation
    return pref_collation