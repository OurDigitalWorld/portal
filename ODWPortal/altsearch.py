__author__ = 'walter'

import urllib
import re
import json
import xmltodict
from ODWPortal.models import SiteAlternateSearches, SiteSetup
from ODWPortal.querySolr import solr_query, get_search_set
from ODWPortal.utilities import get_doc_block
from Portal.settings import SOLR_URL

def alt_search(site_id, requestQ, action, search_set):
    return_list = []
    #TODO:  suppress search if q is empty (not point of asking for everything
    alt_site_search_set = SiteAlternateSearches.objects.filter(site=site_id).order_by('site_order')
    AltQueryStr, AltQueryDict = solr_query(requestQ, 'extAltSearch', "")
    #print("original search_set:", search_set)
    for alt_site in alt_site_search_set:
        AltPreferredResultsURL = ''
        if alt_site.alt_site_id:
            alt_search_set = alt_site_lookup(alt_site.alt_site_id)
            #print("alt_search_set:", alt_search_set)
            local_queryStr, local_QueryDict = solr_query(requestQ, 'extAltSearch', alt_search_set)
            #print("local_queryStr:", local_queryStr)
            #TODO: get site name from Sites
            AltBaseURL = '%ssearch/select/?wt=json' % SOLR_URL
            ext_query_str = local_queryStr.replace(alt_search_set, '')
            AltPreferredResultsURL = '%sresults?%s' % (alt_site.alt_site_url, ext_query_str)
            #different because we're doing an internal lookup
            #print("AltSearchURL 1: ", AltSearchURL)
        else:
            local_queryStr = AltQueryStr
            AltBaseURL = alt_site.alt_site_url
            AltResultsURL = AltBaseURL  # the same url because the multisearch and the user are searching externally
        alt_dict = {'label': alt_site.alt_site_label}
        if action == 'count':
            #print(alt_site.alt_site_label)
            AltDocsCount, AltDocsURL, AltDocsResults = getAltSearch(
                local_queryStr, AltBaseURL, AltResultsURL, action, '')
            alt_dict.update({'count': AltDocsCount})
            alt_dict.update({'url': AltDocsURL})
            return_list.append(alt_dict)
        elif action == 'results':
            #print("AltSearchURL2: ", AltSearchURL)
            AltDocsCount, AltDocsURL, AltDocsResults = getAltSearch(local_queryStr, AltBaseURL, AltResultsURL, action, alt_site.alt_site_syntax)
            alt_dict.update({'count': AltDocsCount})
            if AltPreferredResultsURL:
                alt_dict.update({'url': AltPreferredResultsURL})
            else:
                alt_dict.update({'url': AltDocsURL})
            alt_dict.update({'results': AltDocsResults})
            if int(AltDocsCount) > 3:
                alt_dict.update({'more': True})
            else:
                alt_dict.update({'more': False})

            return_list.append(alt_dict)
    #print(return_list)
    return return_list


def getAltSearch(queryStr, AltBaseURL, AltResultsURL, action, search_syntax):
    AltDocsCount = 0
    if queryStr:
        #TODO production gov docs/portal fail on phrase searches with ampersands/%26
        queryStr = queryStr.replace('+&+', '+')
        queryStr = queryStr.replace('+%26+', '+')
        queryStr = queryStr.replace('%20%26%20', '+')

        # prep URL for passing as link to user
        AltResultsURL = "%sresults?%s" % (AltResultsURL, queryStr)
        # do internal searches for count or results
        if action == "count":
            if SOLR_URL in AltBaseURL:
                AltCountURL = "%s&%s&rows=0" % (AltBaseURL,queryStr)
            else:
                AltCountURL = "%scount?%s" % (AltBaseURL,queryStr)
            AltDocs = getAltDocs(AltCountURL)
            #print(AltDocs)
        elif action == "results":
            if SOLR_URL in AltBaseURL:
                AltDocsURL = "%s&%s&rows=3" % (AltBaseURL, queryStr)
            else:
                #TODO:  utter hack to deal with solr 1.4 json not escaping unparsedQuery  ... i.e. GovDocs
                queryStr = queryStr.replace("%22",'')
                AltDocsURL = "%s%s?%s&rows=3" % (AltBaseURL,search_syntax, queryStr)
            AltDocs = getAltDocs(AltDocsURL)
            if search_syntax == "rss.xml":
                AltDocsDecode = AltDocs[0].decode(encoding='UTF-8')
                AltDocsResults = xmltodict.parse(AltDocsDecode)
            else:
                AltDocsResults = AltDocs
                try:
                    AltDocsResults = (AltDocsResults[0].decode(encoding='UTF-8'))
                except UnicodeDecodeError:
                    AltDocsResults = (AltDocsResults[0].decode(encoding="ISO-8859-1"))
                AltDocsResults = json.loads(AltDocsResults)
            if 'solr' in AltDocsResults:
                AltDocsCount = AltDocsResults['solr']['json']['response']['numFound']
                count_docs = int(AltDocsCount)
                if count_docs > 0:
                    docs = AltDocsResults['solr']['json']['response']['docs']
                    AltDocsResults= get_doc_block(docs, "", "", "", "eng")
                    #print(AltDocsResults)
            elif AltDocsResults['response']['numFound']:
                AltDocsCount = AltDocsResults['response']['numFound']
                count_docs = int(AltDocsCount)
                if count_docs > 0:
                    docs = AltDocsResults['response']['docs']
                    #print(docs)
                    AltDocsResults= get_doc_block(docs, "", "", "", "eng")
                    #print(AltDocsResults)
            #print(AltDocsCount)
        #AltDocsCountParsableXML = AltDocs[0].decode(encoding='UTF-8')
        try:
            AltDocsCountParsableXML = (AltDocs[0].decode(encoding='UTF-8'))
        except UnicodeDecodeError:
            AltDocsCountParsableXML = (AltDocs[0].decode(encoding="ISO-8859-1"))
        if AltDocsCountParsableXML == 'error!':
            #something stupid happened with the url
            one = 1
        elif AltDocsCountParsableXML.isdigit():
            # if a raw number
            AltDocsCount = AltDocsCountParsableXML
        elif re.search('numFound=', AltDocsCountParsableXML):
            #if a solr xml response
            count_object = re.search('numFound=\"(\d.*?)\"', AltDocsCountParsableXML)
            if count_object:
                AltDocsCount = count_object.group(1)
        elif re.search('numFound\":', AltDocsCountParsableXML):
            #if a solr json response
            count_object = re.search('numFound\":(\d.*?),', AltDocsCountParsableXML)
            if count_object:
                AltDocsCount = count_object.group(1)
    return AltDocsCount, AltResultsURL, AltDocsResults


def getAltDocs(url):
    #print("url: ", url)
    try:
        conn = urllib.request.urlopen(url)
        rdata = []
        chunk = 'xx'
        while chunk:
            chunk = conn.read()
            if chunk:
                rdata.append(chunk)
        AltDocs = rdata
        conn.close()
    except IOError:
        #print 'Cannot open <strong class="highlight">URL</strong> %s for reading' % url
        AltDocs = 'error!'
    return AltDocs

def alt_site_lookup(site_id):
    site_values = SiteSetup.objects.filter(site_id=site_id)
    site_dict = {}
    #print("site values: ", site_values)
    for f in site_values:
       #print("function settings: " + f.afield + ":" + f.avalue)
       site_dict[f.afield] = f.avalue
    alt_search_set = get_search_set(site_dict)
    return alt_search_set