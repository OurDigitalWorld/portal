import json
from urllib.parse import quote
from django.shortcuts import render
from django.http import HttpRequest
import ODWPortal.externalurls
from ODWPortal.utilities import page_navigation, facet_panel, get_doc_block, get_media_label
from ODWPortal.querySolr import search_logic, search_query, facet_query, get_search_set
from Portal.hostdiscovery import site_settings, site_language
from Portal.slideshow import get_slideshow
# from Portal.customlog import log_request


def index(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    # print(site_lang['page_name_search'])
    block = site_values['search_content_block']
    block_list = site_values['search_content_block_li']
    search_content_block_rev = block.replace("LI_XXXXX_LI", block_list)
    encoded_url = quote(HttpRequest.build_absolute_uri(request))
    page_name = '%s: %s' % (site_lang['NBLabelSearchForm'], site_values['site_name'])
    encoded_page_name = quote(page_name)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'search_content_block_rev': search_content_block_rev,
        'encoded_url': encoded_url,
        'encoded_page_name': encoded_page_name,
    }
    return render(request, 'Portal/search.html', context)


def about(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    encoded_url = quote(HttpRequest.build_absolute_uri(request))
    page_name = '%s: %s' % (site_lang['about_label_page'], site_values['site_name'])
    encoded_page_name = quote(page_name)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'encoded_url': encoded_url,
        'encoded_page_name': encoded_page_name,
    }
    return render(request, 'Portal/about.html', context)


def help_request(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    encoded_url = quote(HttpRequest.build_absolute_uri(request))
    page_name = '%s: %s' % (site_lang['NBLabelHelp'], site_values['site_name'])
    encoded_page_name = quote(page_name)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'encoded_url': encoded_url,
        'encoded_page_name': encoded_page_name,
    }
    return render(request, 'Portal/help.html', context)


def contributors(request):
    site_values = site_settings(request)
    site_lang = site_language(site_values['language'])
    search_set = get_search_set(site_values)
    contribute_display = site_values['ContributorsListDisplay']
    facet_list = ODWPortal.externalurls.list_facet("site",
                                                   "site",
                                                   'results',
                                                   contribute_display,
                                                   site_lang,
                                                   search_set)
    encoded_url = quote(HttpRequest.build_absolute_uri(request))
    page_name = '%s: %s' % (site_lang['DetLabelContributors'], site_values['site_name'])
    encoded_page_name = quote(page_name)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'facet_list': facet_list,
        'encoded_url': encoded_url,
        'encoded_page_name': encoded_page_name,
        'contribute_display': contribute_display,
    }
    return render(request, "Portal/contributors.html", context)


def mediatype(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    site_lang = site_language(site_values['language'])
    facet_list = ODWPortal.externalurls.media_facet(request.GET, 'results', search_set)
    mt = request.GET['mt']
    media_label = get_media_label(mt, site_lang)
    encoded_url = quote(HttpRequest.build_absolute_uri(request))
    page_name = '%s: %s' % (site_lang['DetLabelMediaType'], site_values['site_name'])
    encoded_page_name = quote(page_name)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'facet_list': facet_list,
        'request': request.GET,
        'mediaLabel': media_label,
        'encoded_url': encoded_url,
        'encoded_page_name': encoded_page_name,
    }
    return render(request, "Portal/mediatypes.html", context)


def results(request):
    search_q = ''
    just_q = ''
    search_logic_string = ''
    q_logic = ''
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    site_lang = site_language(site_values['language'])
    request_q = request.GET.copy()
    (solr_response,
     num_found,
     rows,
     page_num,
     docs,
     facets,
     query_dict) = ODWPortal.externalurls.get_docs(request_q, search_set)
    num_found_int = int(num_found)
    if 'q' in query_dict:
        original_q = query_dict.__getitem__('q')
    else:
        original_q = ''

    # do we need to try again with the spelling suggestions
    if isinstance(query_dict, dict):
        # PartsQ, PartsQD = solr_query(request_q, 'extAltSearch', search_set)
        search_logic_string, q_logic = search_logic(query_dict, site_lang, site_values)
        # print('searchLogicString(144): ', searchLogicString)
        search_q, just_q = search_query(query_dict)

    # Check for number of records for search criteria with lat/long values and
    docs = solr_response['response']['docs']
    highlighting = solr_response['highlighting']
    document_panel = get_doc_block(docs, just_q, highlighting, 'resultView', site_lang, site_values)
    int_rows = int(rows)
    page_nav_bar = page_navigation(num_found_int, int_rows, page_num, search_q, site_lang)
    facet_panels = facet_panel(facets, search_q, site_lang, query_dict)
    facet_q = facet_query(query_dict)

    encoded_url = quote(HttpRequest.build_absolute_uri(request))
    page_name = '%s: %s' % (site_lang['NBLabelResults'], site_values['site_name'])
    encoded_page_name = quote(page_name)
    context = {
        'site_values': site_values,
        'site_language': site_lang,
        'encoded_url': encoded_url,
        'encoded_page_name': encoded_page_name,
        "document_panel": document_panel,
        "facet_panels": facet_panels,
        "num_found": num_found,
        "page_nav_bar": page_nav_bar,
        "search_logic_string": search_logic_string,
        "query_logic": q_logic,
        'original_q': original_q,
        "search_q": search_q,
        "facet_q": facet_q,
    }
    return render(request, "Portal/results.html", context)


def xml(request, xml_type):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    solr_response = ODWPortal.externalurls.get_xml(request.GET, xml_type, search_set)
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
        "site_list": site_list,
        "media_type_list": media_type_list
    })


def count(request):
    site_values = site_settings(request)
    search_set = get_search_set(site_values)
    result_count = ODWPortal.externalurls.get_count(request.GET, search_set)
    mime_str = "text/plain"
    return render(request, "Portal/xml.html", {"solrResponse": result_count}, content_type=mime_str)


def slideshow(request):
    response = get_slideshow(request)
    mime_str = "text/plain"
    return render(request, "Portal/xml.html", {"solrResponse": response}, content_type=mime_str)
