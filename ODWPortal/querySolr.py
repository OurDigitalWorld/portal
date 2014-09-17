__author__ = 'walter'

import urllib
from urllib.parse import urlencode
from django.utils.http import urlquote
from ODWPortal.utilities import get_media_label

#constants
defaultRows = 20
facetURL = ('&fl=id,title,titleSort,thumbnail,url,localid,description,'
            'site,type,featureComment,featureMystery,bibliographicCitation,'
            'accessionNo,madePublic,publicDisplay,creator,contributor,'
            'publisher,itemLatitude,itemLongitude,subject,source,language,'
            'spatial,temporal,created,modified,enclosureURL,enclosureLength,'
            'enclosureType,multiPart'
            '&facet=true'
            '&facet.field=type'
            '&f.type.facet.sort=index'
            '&facet.field=fSpatial'
            '&f.fSpatial.facet.missing=true'
            '&f.fSpatial.mincount=1'
            '&facet.field=fGroupName'
            '&f.fGroupName.mincount=1'
            '&facet.field=site'
            '&facet.field=itemType'
            '&facet.field=featureComment'
            '&facet.field=featureMystery'
            '&facet.field=fDateDecade'
            '&f.fDateDecade.facet.sort=index'
            '&facet.field=fDateYear'
            '&f.fDateYear.facet.sort=index'
            '&facet.mincount=1'
            '&facet.limit=-1'
            '&facet.sort=true'
            '&facet.zeros=false'
            '&spellcheck=true'
            '&spellcheck.collate=true'
            '&hl=on&hl.fragsize=75'
            '&hl.snippets=2'
            '&hl.fl=fulltext,description'
            '&hl.simple.pre=<b>'
            '&hl.simple.post=</b>'
            '&spellcheck.extendedResults=true'
            '&spellcheck.count=10')
#


def solr_query(request, xml_type, search_set):
    """
    parses request values and aligns them with the related solr fields
    request is derived from GET object
    xmlType:  kml, extAltSearch, vitaAltSearch, count, xml
            (where xml is ordinary search)
    returns a queryString value for searching solr, and a
        tuned queryDict with the search values
    """
    nvps = request.copy()
    query_str = '&q='
    spell_q = ''
    query_s = ''
    query_dict = {}
    if nvps.__contains__('q') or nvps.__contains__('q2'):
        query_s, return_str, facet_form_str, spell_q = parse_q(nvps, query_dict)
        query_str += query_s
    if xml_type == 'extAltSearch':
        # external Alternate Searches are only passed the q/q2 values
        query_str = 'q=%s+%s' % (query_s, search_set)
    else:
        # need to process the rest of the request values
        if nvps.__contains__('id'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'id', 'id', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['id'] = ''
        if nvps.__contains__('site'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'site', 'site', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['site'] = ''
        if nvps.__contains__('mt'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'mt', 'type', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['mt'] = ''
        if nvps.__contains__('lc'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'lc', 'fSpatial', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['lc'] = ''
        if nvps.__contains__('itype'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'itype', 'itemType', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['itype'] = ''
        if nvps.__contains__('grn'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'grn', 'fGroupName', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['grn'] = ''
        if nvps.__contains__('dd'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'dd', 'fDateDecade', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['dd'] = ''
        if nvps.__contains__('dy'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'dy', 'fDateYear', 'or', query_dict)
            query_str += query_s
        else:
            query_dict['dy'] = ''
        if nvps.__contains__('fc'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'fc', 'featureComment', '', query_dict)
            query_str += query_s
        else:
            query_dict['fc'] = ''
        if nvps.__contains__('fm'):
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, 'fm', 'featureMystery', '', query_dict)
            query_str += query_s
        else:
            query_dict['fm'] = ''
        latitude_search_q = '+itemLatitude:[*+TO+*]'
        if xml_type == 'kml':
            query_str += latitude_search_q
            kml_query_str = ''
        else:
            kml_query_str = query_str+ latitude_search_q

        if xml_type == 'count':
            query_str += '+%s' % search_set
        else:
            query_str += '+%s%s' % (search_set, facetURL)

        if spell_q:
            #spellQ = spellQ.replace(' ', '+')
            query_str += '&spellcheck.q=%s~0.5' % urlquote(spell_q)

        if xml_type == 'kml':
            rows = 200
        elif xml_type == 'count':
            rows = 0
        elif "rows" in request:
            rows = int(request.__getitem__('rows'))
        else:
            rows = defaultRows
        query_str += '&rows=%s' % rows
        if "p" in request:
            page = int(request.__getitem__('p'))
            start = (page - 1) * rows
            query_str += '&start=%s&p=%s' % (start, page)
        #TODO need dictionary of inbound field values (e.g. 'bl')
        # and corresponding content to process as unparsed query (DONE),
        # as query set for facet search and for results display (part DONE
    return query_str, query_dict


def parse_q(nvps, query_dict):
    return_str = ''
    facet_form_str = ''
    query_merge = ''
    query = ''
    spell_q = ''
    if nvps.__contains__('q'):
        query = nvps.getlist('q')
        #if multiple values for 'q' join into space delimited string
        query_merge = ' '.join(query)
        query_merge = query_merge.replace('  ', ' ')
        query_merge = query_merge.strip()
        query_dict['q'] = query_merge
        spell_q = query_merge
        query_dict['spellcheck.q'] = query_merge
        if len(query_merge) > 0:
            #if fz > 0 then insert modifiers
            if nvps.__contains__('fz'):
                fz = nvps.__getitem__('fz')
                if fz == '1':
                    fz_modifier = '~0.70'
                elif fz == '2':
                    fz_modifier = '~0.60'
                elif fz == '3':
                    fz_modifier = '~0.50'
                else:
                    fz_modifier = ''
                query_merge = query_merge.replace(' ', fz_modifier + ' ')+fz_modifier
                if fz != '0':
                    query_dict['fz'] = fz
            else:
                query_dict['fz'] = ''
            #if bl == 'or' then insert ' OR '
            if nvps.__contains__('bl'):
                bl = nvps.__getitem__('bl')
                if bl == 'or':
                    query_merge = query_merge.replace(' ', ' OR ')
                elif bl == 'phrase':
                    #do something else
                    query_merge = '"%s"' % query_merge
                if bl != 'and':
                    query_dict['bl'] = bl
            else:
                query_dict['bl'] = ''
            #if st (structured query)  narrow search by field
            if nvps.__contains__('st'):
                st = nvps.__getitem__('st')
                if st == 'ti':
                    query_merge = 'title:%s' % query_merge
                if st == 'su':
                    query_merge = 'subject:%s' % query_merge
                    # TODO test HPL metadata for creator using 'Henley' search
                if st == 'au':
                    query_merge = '((creator:%s) OR (contributor:%s))' % (query_merge, query_merge)
                if st == 'ac':
                    query_merge = 'accessionNo:%s' % query_merge
                if st == 'sr':
                    query_merge = 'source:%s' % query_merge
                if st == 'md':
                    query_merge = 'text:%s' % query_merge
                query_dict['st'] = st
            else:
                query_dict['st'] = ''
        else:
            query_dict['q'] = ''

    else:
        query_dict['q'] = ''

    if nvps.__contains__('q2'):
        #q2 already prepped
        q2 = nvps.__getitem__('q2')
        if query:   # append to query
            query_merge = '(%s) AND %s' % (query_merge, q2)
        else:       # q2 is our only query statement
            query_merge = q2
    else:
        query_dict['q2'] = ''

    query_dict['q2'] = query_merge
    queryStr = urlquote(query_merge)
    #queryStr = queryMerge
    #TODO return returnStr/facetFormStr as a dictionary and then parse into appropriate HTML
    return queryStr, return_str, facet_form_str, spell_q


def parse_nvp(nvps, search_field, solr_field, boolean, query_dict):
    facet_form_str = ''
    return_str = ''
    query_str = ''
    value_list = nvps.getlist(search_field)
    #TODO the following two lines are a complete hack to deal
    # with zero length "lists" being returned
    if len(value_list) == 1 and len(value_list[0]) == 0:
        nothing = 0
    else:
        if boolean == 'or':
            value = '" OR "'.join(value_list)
        else:
            value = ' '.join(value_list)
        query_str = '+%s:("%s")' % (solr_field, urlquote(value))
        query_dict[search_field] = value

    return query_str, return_str, facet_form_str


def search_logic(response_query_dict, site_language):
    logic = ''
    qd = response_query_dict
    if qd.get('st'):
        st = qd['st']
        if st == 'ti':
            logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsTitle']
        elif st == 'su':
            logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsSubject']
        elif st == 'au':
            logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsCreator']
        elif st == 'ac':
            logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsIdentifier']
        elif st == 'kw':
            logic += '<b>%s:</b> ' % site_language['AdvLabelKeyword']
    elif qd.get('q2'):
            logic += '<b>%s:</b> ' % site_language['AdvLabelKeyword']
    if qd.get('q2'):
        q2 = qd['q2']
        #print 'searchLogic1: q2: %s' % q2
        q2 = q2.replace('+', ' ')
        q2 = urllib.parse.unquote(q2)
        #print 'searchLogic2: q2: %s' % q2
        #q2 = q2.replace('%20', ' ')
        #q2 = q2.replace('%22', '"')
        logic += q2 + '&#160;&#160;'
    if qd.get('fz'):
        fz = qd['fz']
        if fz == '1':
            logic += ' <b>%s</b> ' % site_language['AdvLabelFuzzyFuzzy']
        elif fz == '2':
            logic += ' <b>%s</b> ' % site_language['AdvLabelFuzzyFuzzier']
        elif fz == '3':
            logic += ' <b>%s</b> ' % site_language['AdvLabelFuzzyFuzziest']
    if qd.get('site'):
        logic += logic_label(site_language['ResFacetContributorsLabelTitle'], qd['site'], site_language)
    if qd.get('mt'):
        logic += logic_label(site_language['ResFacetMediaTypesLabelTitle'], qd['mt'].title(), site_language)
    if qd.get('lc'):
        logic += logic_label(site_language['AdvLabelLocation'], qd['lc'], site_language)
    if qd.get('itype'):
        logic += logic_label(site_language['ResLogicItemTypeLabel'], qd['itype'], site_language)
    if qd.get('grn'):
        logic += logic_label(site_language['AdvLabelGroups'], qd['grn'], site_language)
    if qd.get('fm'):
        logic += '<b>%s</b>: True ' % site_language['AdvLabelMystery']
    if qd.get('fc'):
        logic += '<b>%s</b>: True ' % site_language['AdvLabelComment']
    if qd.get('dd'):
        logic += logic_label(site_language['ResLogicDecadeLabel'], qd['dd'], site_language)
    if qd.get('dy'):
        logic += logic_label(site_language['ResLogicYearLabel'], qd['dy'], site_language)
    if qd.get('da'):
        logic += logic_label(site_language['AdvLabelBetweenDatesAfter'], qd['da'], site_language)
    if qd.get('db'):
        logic += logic_label(site_language['AdvLabelBetweenDatesBefore'], qd['db'], site_language)
    if qd.get('dt'):
        logic += logic_label('Date ', qd['dt'], site_language)

    #print 'searchLogic2: strLogic: %s' % strLogic
    return logic


def logic_label(label, value, site_language):
    if label == site_language['ResFacetMediaTypesLabelTitle']:
        value = get_media_label(value, site_language)
    return_str = ' <b>%s</b> %s&#160;&#160;' % (label, str(value).replace('" OR "', ' or '))
    return return_str


def search_query(response_query_dict):
    search_q = ''
    just_q = ''
    for key, value in response_query_dict.items():
        if value:
            if key != 'q' and key != 'spellcheck.q':
                if search_q:
                    search_q += "&amp;"
                search_q += '%s=%s' % (key, urlquote(value))
            if key == 'q2':
                just_q = '%s' % (urlquote(value))
    return search_q, just_q


def facet_query(response_query_dict):
    """
    prepare hidden fields to qualify facet search
    """
    facet_q = ''
    for key, value in response_query_dict.items():
        if value:
            if key != 'q':
                facet_q += '<input type="hidden" name="%s" value="%s"/>' % (key, value)
    return facet_q


def get_search_set(site_values):
    search_set = ''
    if 'search_set' in site_values:
        search_set = "searchSet:%s" % site_values['search_set']
    if 'SiteSearchScope' in site_values:
        search_scope = site_values['SiteSearchScope']
        search_set += string_search_scope(search_scope)
    if 'record_owner' in site_values:
        ro = site_values['record_owner']
        search_set += 'recordOwner:(%s)' % urllib.parse.quote(ro)
    #print("SolrQuery(337): ", search_set)
    return search_set


def string_search_scope(search_scope):
    if search_scope:
        ss_query = '+'
        ss_field, ss_value = search_scope.split('=')
        if ss_value[:4] == 'not_':
            ss_query += "NOT+"
        if ss_field == 'smt':
            ss_query += 'type:'
        elif ss_field == 'sgrd':
            ss_query += 'groupID:'
        if ss_value[:4] == 'not_':
            ss_query += ss_value[4:]
        else:
            ss_query += ss_value
        return ss_query
