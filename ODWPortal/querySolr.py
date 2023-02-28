__author__ = 'walter'

import urllib
from urllib.parse import quote_plus
from ODWPortal.utilities import get_media_label
# from Portal.customlog import log_request

# constants
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
            '&facet.field=rightsCreativeCommons'
            '&f.fDateDecade.facet.sort=index'
            '&facet.field=fDateYear'
            '&f.fDateYear.facet.sort=index'
            '&facet.mincount=1'
            '&facet.limit=-1'
            '&facet.sort=true'
            '&facet.zeros=false'
            '&hl=on&hl.fragsize=75'
            '&hl.snippets=2'
            '&hl.fl=fulltext,description'
            '&hl.simple.pre=<b>'
            '&hl.simple.post=</b>')

field_dictionary = {
    'id': ['id', 'id', 'or'],
    'site': ['site', 'site', 'or'],
    'mt': ['mt', 'type', 'or'],
    'lc': ['lc', 'fSpatial', 'or'],
    'itype': ['itype', 'itemType', 'or'],
    'grn': ['grn', 'fGroupName', 'or'],
    'grd': ['grd', 'groupid', 'or'],
    'dd': ['dd', 'fDateDecade', 'or'],
    'dy': ['dy', 'fDateYear', 'or'],
    'fc': ['fc', 'featureComment', ''],
    'fm': ['fm', 'featureMystery', ''],
    'fcc': ['fcc', 'rightsCreativeCommons', '']
}

def solr_query(request, xml_type, search_set):
    """
    parses request values and aligns them with the related solr fields
    request is derived from GET object
    xmlType:  extAltSearch, vitaAltSearch, count, xml
            (where xml is ordinary search)
    returns a queryString value for searching solr, and a
        tuned queryDict with the search values
    """
    nvps = request.copy()
    query_str = '&q=('
    query_dict = {}
    if nvps.__contains__('q'):
        query_s, return_str, facet_form_str = parse_q(nvps, query_dict)
        query_str += query_s
    for nvps_key in nvps:
        if nvps_key in field_dictionary:
            nvps_values = field_dictionary.get(nvps_key)
            (query_s,
             return_str,
             facet_form_str) = parse_nvp(nvps, nvps_values[0], nvps_values[1], nvps_values[2], query_dict)
            query_str += query_s
    if xml_type == 'count':
        query_str = '%s)+AND+(%s)' % (query_str, search_set)
    else:
        query_str = '%s)+AND+(%s)%s' % (query_str, search_set, facetURL)
    if xml_type == 'count':
        rows = 0
    elif "rows" in request:
        rows = int(request.__getitem__('rows'))
        if rows > 200:
            rows = 200
    else:
        rows = defaultRows
    query_dict['rows'] = str(rows)
    query_str += '&rows=%s' % rows
    if "p" in request:
        page = int(request.__getitem__('p'))
        start = (page - 1) * rows
        query_str += '&start=%s&p=%s' % (start, page)
    return query_str, query_dict


def parse_q(nvps, query_dict):
    return_str = ''
    facet_form_str = ''
    query_merge = ''
    # query = ''
    if nvps.__contains__('q'):
        query = nvps.getlist('q')
        # if multiple values for 'q' join into space delimited string
        query_merge = ' '.join(query)
        query_merge = query_merge.replace(':', ' ')
        query_merge = query_merge.replace(';', ' ')
        query_merge = query_merge.replace('  ', ' ')
        query_merge = query_merge.strip()
        query_dict['q'] = query_merge
        if len(query_merge) > 0:
            # if fz > 0 then insert modifiers
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
            # if bl == 'or' then insert ' OR '
            if nvps.__contains__('bl'):
                bl = nvps.__getitem__('bl')
                if bl == 'or':
                    query_merge = query_merge.replace(' ', ' OR ')
                elif bl == 'phrase':
                    # do something else
                    query_merge = '"%s"' % query_merge
                if bl != 'and':
                    query_dict['bl'] = bl
            else:
                query_dict['bl'] = ''
            # if st (structured query)  narrow search by field
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

    query_str = quote_plus(query_merge)
    # queryStr = queryMerge
    # TODO return returnStr/facetFormStr as a dictionary and then parse into appropriate HTML
    return query_str, return_str, facet_form_str


def parse_nvp(nvps, search_field, solr_field, boolean, query_dict):
    facet_form_str = ''
    return_str = ''
    query_str = ''
    value_list = nvps.getlist(search_field)
    if value_list:
        if len(value_list[0]) > 0:
            if boolean == 'or':
                value = '" OR "'.join(value_list)
            else:
                value = ' '.join(value_list)
            query_str = '+%s:("%s")' % (solr_field, quote_plus(value))
            query_dict[search_field] = value

    return query_str, return_str, facet_form_str


def search_logic(response_query_dict, site_language, site_values):
    q_logic = ''
    qd = response_query_dict
    q_string = qd.get('q')
    if q_string != '*:*' and q_string != '%2A%3A%2A':
        if qd.get('st'):
            st = qd['st']
            if st == 'ti':
                q_logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsTitle']
            elif st == 'su':
                q_logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsSubject']
            elif st == 'au':
                q_logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsCreator']
            elif st == 'ac':
                q_logic += '<b>%s:</b> ' % site_language['AdvLabelFieldsIdentifier']
            elif st == 'kw':
                q_logic += '<b>%s:</b> ' % site_language['AdvLabelKeyword']
        else:
            q_logic += '<b>%s:</b> ' % site_language['AdvLabelKeyword']
    logic = '<ul>'
    if qd.get('fz'):
        fz = qd['fz']
        if fz == '0':
            logic += ' <b>%s</b> ' % site_language['AdvLabelFuzzyFuzzy']
        elif fz == '2':
            logic += ' <b>%s</b> ' % site_language['AdvLabelFuzzyFuzzier']
        elif fz == '3':
            logic += ' <b>%s</b> ' % site_language['AdvLabelFuzzyFuzziest']
    if qd.get('site'):
        site = qd.get('site')
        if site:
            logic += logic_label(site_language['ResFacetContributorsLabelTitle'],
                                 qd, site_language, 'site', site_values)
    if qd.get('mt'):
        logic += logic_label(site_language['ResFacetMediaTypesLabelTitle'],
                             qd, site_language, 'mt', site_values)
    if qd.get('lc'):
        logic += logic_label(site_language['AdvLabelLocation'],
                             qd, site_language, 'lc', site_values)
    if qd.get('itype'):
        logic += logic_label(site_language['ResLogicItemTypeLabel'],
                             qd, site_language, 'itype', site_values)
    if qd.get('grn'):
        logic += logic_label(site_language['AdvLabelGroups'],
                             qd, site_language, 'grn', site_values)
    if qd.get('grd'):
        logic += logic_label(site_language['AdvLabelGroups'],
                             qd, site_language, 'grd', site_values)
    if qd.get('fm'):
        fm = qd.get('fm')
        label = '<b>%s</b> %s ' % (site_language['AdvLabelMystery'], site_language['NBLabelYes'])
        logic += presentable_search_logic(label,
                                          qd, 'fm', fm, site_values)
    if qd.get('fc'):
        fc = qd.get('fc')
        label = '<b>%s</b> %s ' % (site_language['AdvLabelComment'], site_language['NBLabelYes'])
        logic += presentable_search_logic(label,
                                          qd, 'fc', fc, site_values)
    if qd.get('dd'):
        logic += logic_label(site_language['ResLogicDecadeLabel'],
                             qd, site_language, 'dd', site_values)
    if qd.get('dy'):
        logic += logic_label(site_language['ResLogicYearLabel'],
                             qd, site_language, 'dy', site_values)
    if qd.get('dr'):
        date_range = qd.get('dr')
        # log_request('after dra logic', date_range)
        if date_range[0] == 'b':
            logic += '<div id="betweendatesbuiltlabel">%s</div>: ' % site_language['AdvLabelBetweenDatesBuilt']
        elif date_range[0] == 'f':
            logic += '<div id="betweendatesfinishedlabel">%s</div>: ' % site_language['AdvLabelBetweenDatesFinished']
    if qd.get('da'):
        logic += logic_label(site_language['AdvLabelBetweenDatesAfter'],
                             qd, site_language, 'da', site_values)
    if qd.get('db'):
        logic += logic_label(site_language['AdvLabelBetweenDatesBefore'],
                             qd, site_language, 'db', site_values)
    if qd.get('dt'):
        logic += logic_label('Date ',
                             qd, site_language, 'dt', site_values)
    if qd.get('fcc'):
        logic += logic_label('Creative Commons ',
                             qd, site_language, 'fcc', site_values)
    logic = logic.replace('text:', '')
    logic = logic.replace('(', '')
    logic = logic.replace(')', '')
    return logic, q_logic


def logic_label(label, qd, site_language, field, site_values):
    value = qd[field]
    return_str = ''
    use_key = True
    value_list = split_string_to_list(value)
    for item in value_list:
        if label == site_language['ResFacetMediaTypesLabelTitle']:
            item_string = get_media_label(item, site_language)
        elif field == 'dd':
            item_string = '%s0-%s9' % (item, item)
        else:
            item_string = item
        if use_key:
            logic_str = ' <b>%s:</b> %s' % (label, item_string)
            return_str += presentable_search_logic(logic_str, qd, field, item, site_values)
    return return_str


def presentable_search_logic(logic_str, response_query_dict, field, item, site_values):
    present_list = ''
    search_q = ''
    for key, value in response_query_dict.items():
        value_list = []
        if value:
            if isinstance(value, str):
                value_list = split_string_to_list(value)
            else:
                value_list.append(value)
            for a_value in value_list:
                if (key == field and item != a_value) or \
                        (
                                key != field and key != 'smt' and key != 'sgrd'
                                and a_value != '*:*' and a_value != '%2A%3A%2A'):
                    # print("querySolr (930): key: ", key, ": ", value, " a_value: ", a_value)
                    if search_q:
                        search_q += "&amp;"
                    search_q += '%s=%s' % (key, quote_plus(a_value))
        present_list = '<li><a href="%s/results?%s">' \
                       '<img src="https://images.ourontario.ca/static/img/remove_searchTerm-red.svg" ' \
                       'alt="%s" class="remove" />' \
                       '</a>%s</li>' % (site_values['site_url'], search_q, site_values['LabRemoveSearchTerm'], logic_str)
    return present_list


def split_string_to_list(value_string):
    value_string = value_string.replace('" OR "', '|')
    value = value_string.replace('" AND "', '|')
    value_list = value.split('|')
    return value_list


def search_query(response_query_dict):
    search_q = ''
    just_q = ''
    for key, value in response_query_dict.items():
        # print(key)
        if value:
            if key != 'q2':
                if search_q:
                    search_q += "&amp;"
                search_q += '%s=%s' % (key, quote_plus(value))
            if key == 'q':
                just_q = quote_plus(value)
    return search_q, just_q


def facet_query(response_query_dict):
    """
    prepare hidden fields to qualify facet search
    which has subsequently migrated to the search logic bar 
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
    # print("SolrQuery(337): ", search_set)
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
