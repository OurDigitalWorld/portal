__author__ = 'walter'

import urllib
import re
import json
import xmltodict
from ODWPortal.models import site_alternate_searches, SiteSetup
from ODWPortal.querySolr import solr_query, get_search_set
from ODWPortal.utilities import get_doc_block
from Portal.settings import SOLR_URL


def alt_search(site_id, request_q, action):
    return_list = []
    alt_site_search_set = site_alternate_searches.objects.filter(site=site_id).order_by('site_order')
    alt_query_string, alt_query_dict = solr_query(request_q, 'extAltSearch', "")
    for alt_site in alt_site_search_set:
        alt_preferred_results_url = ''
        if alt_site.alt_site_id:
            alt_search_set = alt_site_lookup(alt_site.alt_site_id)
            local_querystr, local_querydict = solr_query(request_q, 'extAltSearch', alt_search_set)
            altbaseurl = '%ssearch/select/?wt=json' % SOLR_URL
            ext_query_str = local_querystr.replace(alt_search_set, '')
            alt_preferred_results_url = '%sresults?%s' % (alt_site.alt_site_url, ext_query_str)
            #        different because we're doing an internal lookup
        else:
            local_querystr = alt_query_string
            altbaseurl = alt_site.alt_site_url
            altresultsurl = altbaseurl  # the same url because the multisearch and the user are searching externally
        alt_dict = {'label': alt_site.alt_site_label}
        if action == 'count':
            altdocscount, alt_docs_url, altdocsresults = get_alt_search(
                local_querystr,
                altbaseurl,
                altresultsurl,
                action,
                ''
            )
            alt_dict.update({'count': altdocscount})
            alt_dict.update({'url': alt_docs_url})
            return_list.append(alt_dict)
        elif action == 'results':
            altdocscount, alt_docs_url, altdocsresults = get_alt_search(
                local_querystr,
                altbaseurl,
                altresultsurl,
                action,
                alt_site.alt_site_syntax
            )
            alt_dict.update({'count': altdocscount})
            if alt_preferred_results_url:
                alt_dict.update({'url': alt_preferred_results_url})
            else:
                alt_dict.update({'url': alt_docs_url})
            alt_dict.update({'results': altdocsresults})
            if int(altdocscount) > 3:
                alt_dict.update({'more': True})
            else:
                alt_dict.update({'more': False})

            return_list.append(alt_dict)
    return return_list


def get_alt_search(query_string, alt_base_url, alt_results_url, action, search_syntax):
    alt_docs_count = 0
    altdocs = ''
    alt_docs_results = ''
    if query_string:
        # production gov docs/portal fail on phrase searches with ampersands/%26
        query_string = query_string.replace('+&+', '+')
        query_string = query_string.replace('+%26+', '+')
        query_string = query_string.replace('%20%26%20', '+')

        # prep URL for passing as link to user
        alt_results_url = "%sresults?%s" % (alt_results_url, query_string)
        # do internal searches for count or results
        if action == "count":
            if SOLR_URL in alt_base_url:
                altcounturl = "%s&%s&rows=0" % (alt_base_url, query_string)
            else:
                altcounturl = "%scount?%s" % (alt_base_url, query_string)
            altdocs = get_alt_docs(altcounturl)
        elif action == "results":
            if SOLR_URL in alt_base_url:
                alt_docs_url = "%s&%s&rows=3" % (alt_base_url, query_string)
            else:
                # utter hack to deal with solr 1.4 json not escaping unparsedQuery  ... i.e. GovDocs
                if '%22' in query_string:
                    query_string = query_string.replace("%22", '')
                    query_string += '&bl=phrase'
                alt_docs_url = "%s%s?%s&rows=3" % (alt_base_url, search_syntax, query_string)
            altdocs = get_alt_docs(alt_docs_url)
            if search_syntax == "rss.xml":
                alt_docs_decode = altdocs[0].decode(encoding='UTF-8')
                alt_docs_results = xmltodict.parse(alt_docs_decode)
            else:
                alt_docs_results = altdocs
                try:
                    alt_docs_results = (alt_docs_results[0].decode(encoding='UTF-8'))
                except UnicodeDecodeError:
                    alt_docs_results = (alt_docs_results[0].decode(encoding="ISO-8859-1"))
                alt_docs_results = json.loads(alt_docs_results)
            if 'solr' in alt_docs_results:
                alt_docs_count = alt_docs_results['solr']['json']['response']['numFound']
                count_docs = int(alt_docs_count)
                if count_docs > 0:
                    docs = alt_docs_results['solr']['json']['response']['docs']
                    alt_docs_results = get_doc_block(docs, "", "", "", "eng")
            elif alt_docs_results['response']['numFound']:
                alt_docs_count = alt_docs_results['response']['numFound']
                count_docs = int(alt_docs_count)
                if count_docs > 0:
                    docs = alt_docs_results['response']['docs']
                    alt_docs_results = get_doc_block(docs, "", "", "", "eng")
        try:
            alt_docs_count_parsable_xml = (altdocs[0].decode(encoding='UTF-8'))
        except UnicodeDecodeError:
            alt_docs_count_parsable_xml = (altdocs[0].decode(encoding="ISO-8859-1"))
        if alt_docs_count_parsable_xml == 'error!':
            # something stupid happened with the url
            one = 1
        elif alt_docs_count_parsable_xml.isdigit():
            # if a raw number
            alt_docs_count = alt_docs_count_parsable_xml
        elif re.search('numFound=', alt_docs_count_parsable_xml):
            # if a solr xml response
            count_object = re.search('numFound=\"(\d.*?)\"', alt_docs_count_parsable_xml)
            if count_object:
                alt_docs_count = count_object.group(1)
        elif re.search('numFound\":', alt_docs_count_parsable_xml):
            # if a solr json response
            count_object = re.search('numFound\":(\d.*?),', alt_docs_count_parsable_xml)
            if count_object:
                alt_docs_count = count_object.group(1)
    return alt_docs_count, alt_results_url, alt_docs_results


def get_alt_docs(url):
    try:
        conn = urllib.request.urlopen(url)
        rdata = []
        chunk = 'xx'
        while chunk:
            chunk = conn.read()
            if chunk:
                rdata.append(chunk)
        alt_docs = rdata
        conn.close()
    except IOError:
        alt_docs = 'error!'
    return alt_docs


def alt_site_lookup(site_id):
    site_values = SiteSetup.objects.filter(site_id=site_id)
    site_dict = {}
    for f in site_values:
        site_dict[f.afield] = f.avalue
    alt_search_set = get_search_set(site_dict)
    return alt_search_set