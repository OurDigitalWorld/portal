import json
from django.shortcuts import render
from django.http import HttpRequest
import ODWPortal.externalurls
from ODWPortal.utilities import page_navigation, facet_panel, get_doc_block, sort_variables, get_media_label
from ODWPortal.querySolr import search_logic, search_query, facet_query, get_search_set
from ODWPortal.altsearch import alt_search
from Portal.hostdiscovery import site_settings, site_language


def index(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    #print(site_lang['page_name_search'])
    #print(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/search.html', context)


def about(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/about.html', context)


def faq(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/faq.html', context)


def help_request(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/help.html', context)


def searchwidgets(request):
    #the options page
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/searchwidgets.html', context)


def searchwidget(request):
    #the linkable widget
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/searchwidget.html', context)


def kml(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/kml.html', context)


def features(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, 'Portal/features.html', context)


def contributors(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    search_set = get_search_set(site_values)
    facet_list = ODWPortal.externalurls.list_facet("site",
                                                   "site",
                                                   'results',
                                                   'checkbox',
                                                   site_lang,
                                                   search_set)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'facetList': facet_list,
    }
    return render(request, "Portal/contributors.html", context)


def mediatype(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    site_lang = site_language(site_values['language'])
    facet_list = ODWPortal.externalurls.media_facet(request.GET, 'results', search_set)
    mt = request.GET['mt']
    media_label = get_media_label(mt, site_lang)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'facetList': facet_list,
        'request': request.GET,
        'mediaLabel': media_label,
    }
    return render(request, "Portal/mediatypes.html", context)


def results(request, result_type):
    search_q = ''
    just_q = ''
    search_logic_string = ''
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    site_lang = site_language(site_values['language'])
    current_url = HttpRequest.build_absolute_uri(request)
    if "results" in current_url:
        alt_url = current_url.replace('results', 'resultm')
    else:
        alt_url = current_url.replace('resultm', 'results')
    request_q = request.GET.copy()
    if result_type == 'multipane':
        request_q['rows'] = '3'
    (solr_response,
     num_found,
     rows,
     page_num,
     docs,
     facets,
     query_dict) = ODWPortal.externalurls.get_docs(request_q, search_set)
    num_found_int = int(num_found)
    alt_collation = ''
    original_num_found = num_found_int
    if 'q' in query_dict:
        original_q = query_dict.__getitem__('q')
    else:
        original_q = ''

    #do we need to try again with the spelling suggestions
    tried_alt_spelling = False
    if not num_found_int:
        #look to see if there are alternate spellings and run again with those
        suggestions = solr_response['spellcheck']['suggestions']
        i = suggestions.index(u'correctlySpelled')
        correctly_spelled = suggestions[i+1]
        if not correctly_spelled:
            tried_alt_spelling = True
            alt_collation = ODWPortal.externalurls.get_pref_collation(suggestions)
            if alt_collation:
                request_q2 = request_q.copy()
                request_q2.__setitem__('q', alt_collation)

                #re-execute search
                #TODO discover why returned QueryDict => facet panel is
                # retaining the original q value
                #TODO discover why multiple terms generating errors
                (solr_response,
                 num_found,
                 rows,
                 page_num,
                 docs,
                 facets,
                 query_dict_2) = ODWPortal.externalurls.get_docs(request_q2, search_set)
                num_found_int = int(num_found)
                #PartsQ, PartsQD = solr_query(request_q2, 'extAltSearch', search_set)
                search_logic_string = search_logic(query_dict_2, site_lang)
                search_q, just_q = search_query(query_dict_2)
            else:
                #we found no result and no alternate spelling
                #TODO: render an empty results page with a suitable message
                one = 1
        else:
            one = 2
    else:
        #PartsQ, PartsQD = solr_query(request_q, 'extAltSearch', search_set)
        search_logic_string = search_logic(query_dict, site_lang)
        #print('searchLogicString(144): ', searchLogicString)
        search_q, just_q = search_query(query_dict)
    if site_values['use_external_links'] == '1':
        alt_search_results = alt_search(
            site_values['site_id'],
            request_q,
            'results',
            search_set)
    else:
        alt_search_results = ''

    # Check for number of records for search criteria with lat/long values and
    kml_count = ODWPortal.externalurls.get_kml_count(request.GET, search_set)
    docs = solr_response['response']['docs']
    highlighting = solr_response['highlighting']
    document_panel = get_doc_block(docs, just_q, highlighting, 'resultView', site_lang)
    int_rows = int(rows)
    page_nav_bar = page_navigation(num_found_int, int_rows, page_num, search_q, site_lang)
    facet_panels = facet_panel(facets, search_q, site_lang)
    sort_json = sort_variables(facets)
    facet_q = facet_query(query_dict)
    start = solr_response['response']['start']
    context = {
        "document_panel": document_panel,
        "facets": facets,
        "facetPanels": facet_panels,
        "sortJson": sort_json,
        "numFound": num_found,
        "OriginalNumFound": original_num_found,
        "OriginalQ"
        "start": start,
        "rows": rows,
        "pageNum": page_num,
        "pageNavBar": page_nav_bar,
        'alt_search_results': alt_search_results,
        "searchLogicString": search_logic_string,
        "OriginalQ": original_q,
        "searchQ": search_q,
        "altCollation": alt_collation,
        "facetQ": facet_q,
        "KMLCount": kml_count,
        "triedAltSpelling": tried_alt_spelling,
        'site_values': site_values,
        'site_language': site_lang,
        'resultType': result_type,
        'alt_url': alt_url,
    }
    return render(request, "Portal/results.html", context)


def results_xml(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    querystring = request.META['QUERY_STRING']
    solr_xml = ODWPortal.externalurls.get_html(request.GET, querystring, 'en', search_set)
    return render(request, "Portal/resultsXML_en.html", {"solrResponse": solr_xml})


def xml(request, xml_type):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    solr_response = ODWPortal.externalurls.get_xml(request.GET, xml_type, search_set)
    if xml_type == 'kml':
        mime_str = "application/vnd.google-earth.kml+xml"
    else:
        mime_str = "text/xml"
    return render(request,
                  "Portal/xml.html",
                  {"solrResponse": solr_response},
                  content_type=mime_str)


def json_handler(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    json_response = ''
    solr_response = ODWPortal.externalurls.get_json(request.GET, search_set)
    if isinstance(solr_response, dict):
        json_response = json.dumps(solr_response, ensure_ascii=False)
    else:
        print("still clueless")
    return render(request,
                  "Portal/xml.html",
                  {"solrResponse": json_response},
                  content_type="application/json")

 
def opensearch(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    context = {
        'site_values': site_values,
        'site_language': site_lang,
    }
    return render(request, "opensearch.xml", context,  content_type="text/xml")


def advsearch(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    site_lang = site_language(site_values['language'])
    site_list = ODWPortal.externalurls.list_facet("site",
                                                  "site",
                                                  'results',
                                                  'option',
                                                  site_lang,
                                                  search_set)
    media_type_list = ODWPortal.externalurls.list_facet("type",
                                                        'mt',
                                                        'results',
                                                        'checkbox',
                                                        site_lang,
                                                        search_set)
    return render(request, "Portal/advsearch.html", {
        'site_values': site_values,
        'site_language': site_lang,
        "siteList": site_list,
        "mediaTypeList": media_type_list
    })


def count(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    result_count = ODWPortal.externalurls.get_count(request.GET, search_set)
    mime_str = "text/plain"
    #using the xml template because we can drop in a raw response, in this case just an integer
    return render(request, "Portal/xml.html", {"solrResponse": result_count}, content_type=mime_str)

def unapi(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    mime_str = "application/xml"
    if request.GET.get('format'):
        xml_type = request.GET.get('format')
        solr_response = ODWPortal.externalurls.get_xml(request.GET, xml_type, search_set)
        return render(request,
                      "Portal/xml.html",
                      {"solrResponse": solr_response},
                      content_type=mime_str)
    elif request.GET.get('id'):
        unapi_id = request.GET.get('id')
        context = {
            "unapi_id": unapi_id,
        }
        return render(request, "Portal/unapi.xml", context, content_type=mime_str)
    else:
        return render(request, "Portal/unapi.xml", content_type=mime_str)
