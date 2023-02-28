import math
import re
from urllib import request, parse
from datetime import datetime
from django.utils.html import escape
from django.template.defaultfilters import truncatewords, striptags
from Portal.settings import STATIC_URL, SOLR2_URL, SNIPPET_URL_OOI, SNIPPET_URL_MHGL
from ODWPortal.parts import get_solr
# from Portal.customlog import log_request

base_results_url = '<a href="results?'
base_parts_url = ('%svitaParts/select?wt=json'
                  '&hl=on'
                  '&hl.fl=text'
                  '&fl=id,docid,partSort,partURL,label'
                  '&hl.fragsize=75'
                  '&start=0'
                  '&rows=10'
                  '&q=') % SOLR2_URL


def page_navigation(num_found, rows, page_number, search_qs, site_language):
    """
    establish the page navigation block for results
    """
    if page_number.isdigit():
        page_number = int(page_number)
    base_page_url = '%s%s&amp;p=' % (base_results_url, search_qs)
    if num_found > 0:
        total_pages = int(math.ceil(float(num_found) / float(rows)))
        page_string = '<span>%s %s %s %s</span>&#160;' % (
            site_language['ResLabelPageBefore'],
            str(page_number),
            site_language['ResLabelPageMiddle'],
            str(total_pages)
        )
        if page_number > 1:
            prev_page = str(page_number - 1)
            page_string += '%s%s"> &#x2190; %s</a>' % (base_page_url, prev_page, site_language['NBLabelPrev'])
        if (page_number - 3) > 0:
            page_string += '%s1">1</a>' % base_page_url
        if (page_number - 3) > 1:
            page_string += '%s2">2</a>' % base_page_url
        if (page_number - 3) > 2:
            page_string += " ... "
        if (page_number - 2) > 0:
            prev_page = str(page_number - 2)
            page_string += '%s%s">%s</a>' % (base_page_url, prev_page, prev_page)
        if (page_number - 1) > 0:
            prev_page = str(page_number - 1)
            page_string += '%s%s">%s</a>' % (base_page_url, prev_page, prev_page)
        if total_pages != 1:
            page_string += '<span class="big">%s</span>' % (str(page_number))
        if page_number < total_pages:
            next_page = str(page_number + 1)
            page_string += '%s%s">%s</a>' % (base_page_url, next_page, next_page)
        if (page_number + 1) < total_pages:
            next_page = str(page_number + 2)
            page_string += '%s%s">%s</a>' % (base_page_url, next_page, next_page)
        if (page_number + 2) < (total_pages - 2):
            page_string += " ... "
        if (page_number + 2) < (total_pages - 1):
            next_page = str(total_pages - 1)
            page_string += '%s%s">%s</a>' % (base_page_url, next_page, next_page)
        if (page_number + 3) < (total_pages + 1):
            next_page = str(total_pages)
            page_string += '%s%s">%s</a>' % (base_page_url, next_page, next_page)
        if page_number < total_pages:
            next_page = str(page_number + 1)
            page_string += '%s%s"> &#x2192; %s</a>' % (base_page_url, next_page, site_language['NBLabelNext'])
    else:
        page_string = ''
    return page_string


def get_doc_block(docs, just_qs, highlighting, block_id, site_language, site_values):
    """
    prep document block for the results page; insert multipage lookups if required
    """
    # log_request("just_qs Utility 85", just_qs)
    # docs is a single item list, containing a dictionary with the elements
    if block_id:
        block_id_string = ' id="%s"' % block_id
    else:
        block_id_string = ''
    if 'SiteGraphicsSet' in site_values:
        site_graphics_set = site_values['SiteGraphicsSet']
    else:
        site_graphics_set = 'A'
    # TODO should the following class actually be single, or dropped?
    doc_block = '<ul%s class="single">' % block_id_string
    for doc in docs:
        doc_id = doc.get("id", "")
        url = doc.get("url", "")
        if isinstance(url, list):
            url = url[0]
        thumbnail = doc.get("thumbnail", "")
        if 'THL_mt' in thumbnail:
            substitute_thumb = '%s_THL_mt' % site_graphics_set
            thumbnail = thumbnail.replace('THL_mt', substitute_thumb)
        title_list = doc.get("title", "")
        if title_list:
            title = title_list[0]
        else:
            title = ''
        type_list = doc.get("type", "")
        # now parse typelist into series of icons
        type_block = ''
        for dctype in type_list:
            icon = type_icons(dctype, 'icon')
            if icon:
                type_block += '<img src="%s" alt="%s" class="img-icon"/>' % (type_icons(dctype, 'icon'), dctype)
        #  feature icons
        feature_mystery = doc.get("featureMystery")
        if feature_mystery:
            type_block += '<img src="%s" alt="mystery" class="img-icon"/>' % type_icons('mystery', 'icon')
        feature_comment = doc.get("featureComment")
        if feature_comment:
            type_block += '<img src="%s" alt="comment" class="img-icon"/>' % type_icons('comment', 'icon')
        # bibliographic Citation
        bibliographic_citation_list = doc.get("bibliographicCitation", "")
        if bibliographic_citation_list:
            bibliographic_citation = bibliographic_citation_list[0]
            # drop bc if it matches the title exactly
            if bibliographic_citation == title:
                bibliographic_citation = ''
        else:
            bibliographic_citation = ''
        # get highlighting if available
        description_block = ''
        if highlighting:
            highlight_dict = highlighting[doc_id]
        else:
            highlight_dict = {}
        if 'fulltext' in highlight_dict:
            highlight = highlight_dict['fulltext']
            description_block = '...%s...' % str(highlight[0])
        elif 'description' in highlight_dict:
            highlight = highlight_dict['description']
            description_block = '...%s...' % str(highlight[0])
            # print descBlock
        else:
            # truncated descriptions
            description_list = doc.get("description", "")
            for desc in description_list:
                description_block = '%s   ' % truncatewords(desc, 50)
        description_block = description_block.replace('&amp;# 160;', ' ')

        # lat/long  not currently used but anticipated in Vita migration
        # latitude = doc.get("itemLatitude","")
        # longitude = doc.get("itemLongitude","")

        # site(s)
        site_list = doc.get("site", "")
        site_block = '<div class="site">'
        for site in site_list:
            site_block += '<strong>%s</strong><br/>' % site
        site_block += '</div>'

        # log_request("multi_part", doc.get("multiPart"))
        # multipart block
        multi_part = doc.get("multiPart")
        multi_part_block = ''
        if multi_part and just_qs:
            # log_request("doing a multiPart lookup:", url)
            (multi_part_block,
             scan_description_block) = multi_part_lookup(just_qs,
                                                         doc_id,
                                                         url,
                                                         site_language)
            if scan_description_block:
                description_block = scan_description_block

        # now assemble
        doc_block += '<li>'
        doc_block += ('<div class="thumbbox" about="%s">'
                      '<a href="%s">'
                      '<img src="%s"  alt="%s" title="%s" />'
                      '</a></div>' %
                      (url, url, thumbnail, escape(striptags(title)), escape(striptags(title))))
        doc_block += ('<abbr class="unapi-id" title="%s" ></abbr>'
                      '<span property="dc:title"><a href="%s">%s</a></span>'
                      % (doc_id, url, escape(title)))
        if block_id:
            doc_block += ('<div class="description" property="dc:description">'
                          '%s &#160;%s  &#160;  &#160; %s %s'
                          '</div>'
                          % (type_block, bibliographic_citation, description_block, multi_part_block))
            doc_block += ('<div class="description_truncate">%s &#160;%s &#160; %s</div>'
                          % (type_block, bibliographic_citation, truncatewords(description_block, 30)))
        else:
            doc_block += ('<div class="description">%s &#160;%s &#160; %s</div>'
                          % (type_block, bibliographic_citation, truncatewords(description_block, 30)))
        doc_block += site_block
        doc_block += '</li>'
    doc_block += '</ul>'
    return doc_block


def multi_part_lookup(just_qs, docid, record_url, site_language):
    # print("justqs: ", just_qs)
    # print(docid)
    # print('recordurl: %s' % recordurl)
    block = ''
    scan_description_block = ''

    url = '%s(%s)+AND+docid:%s&sort=partSort+asc' % (base_parts_url, just_qs, docid)

    # log_request("parturl:", url)
    solr_response = get_solr(url, 'json')
    # log_request("solr_response: ", solr_response)
    if isinstance(solr_response, dict):
        parts_count = solr_response['response']['numFound']
        if parts_count > 0:
            block = '<div class="docParts"><div class="docPartsLabel">%s:</div>' % site_language['ResLabelPage']
            # print url
            parts = solr_response['response']['docs']
            # parts = [x['docs'] for x in solr_response['response']]
            first_pass = True
            # scan_description_block = ''
            for part in parts:
                part_url = part.get('partURL')
                label_list = part.get('label')
                label = label_list[0]
                label = label.replace("['", "")
                label = label.replace("']", "")
                part_id = part.get('id')
                # print("id: ", part_id)
                doc_id = part.get('docid')
                if 'text' in solr_response['highlighting'][part_id]:
                    highlight = striptags(solr_response['highlighting'][part_id]['text'][0])
                else:
                    highlight = ''
                part_sort = part.get('partSort')
                use_url = ''
                if '/data' in record_url:
                    # print 'partURL (data): %s' % partURL
                    index = record_url.index('data')
                    # print index
                    base_record_url = record_url[:index]
                    # print(base_record_url)
                    use_url = '%spage/%s?q=%s&amp;docid=%s' % (base_record_url, part_sort, just_qs, doc_id)
                elif 'http:' in part_url:
                    # print 'partURL (http): %s' % partURL
                    use_url = '%s&amp;query=%s' % (part_url, just_qs)
                if first_pass:
                    # if using graphic block from ink get that prepared
                    # print 'part_url (first pass): %s' % part_url
                    base_url = ''
                    if 'ink' in part_url or '/page/' in part_url:
                        if 'OOI' in part_id:  # has to be directed to one of two databases/services
                            base_url = SNIPPET_URL_OOI
                        elif 'MHGL' in part_id:
                            base_url = SNIPPET_URL_MHGL
                        if 'AND' in just_qs:  # replace AND with OR for the OCR index search
                            snippet_qs = just_qs.replace('AND', 'OR')
                        else:
                            snippet_qs = just_qs
                        snippet_url = '%s?id=%s&q=%s' % (base_url, part_id, snippet_qs)
                        # print('snippet_url: ', snippet_url)
                        try:
                            conn = request.urlopen(snippet_url)
                            scan_description_block = conn.read().decode('utf-8')
                            conn.close()
                        except IOError:
                            scan_description_block = ''
                            # To Do: fix by passing the preferred url for the site
                            # to a  snippet2.asp where we can derive the site id from the url
                first_pass = False
                block += ('<div class="docPart">'
                          '<a href="%s" title="... %s ...">'
                          '%s</a>'
                          '</div> '
                          % (use_url, highlight, label))
            if parts_count > 10:
                more_href = ''
                block += ('<div class="docPartAll">'
                          '<a href="%s" title="%s">'
                          '[%s %s %s]'
                          '</a>'
                          '</div>'
                          % (more_href, site_language['ResLabelPageMore'],
                             site_language['ResLabelPageEntire1'], parts_count,
                             site_language['ResLabelPageEntire2']))

            block += '</div>'
    return block, scan_description_block


def facet_panel(facets, search_qs, site_language, query_dict):
    facet_string = '<div id="facetPanels">'
    dctype = facets['type']
    site = facets['site']
    fspatial = facets['fSpatial']
    fgroupname = facets['fGroupName']
    item_type = facets['itemType']
    feature_comment = facets['featureComment']
    feature_mystery = facets['featureMystery']
    decades = facets['fDateDecade']
    rights_creative_commons = facets['rightsCreativeCommons']
    if site:
        facet_string += facet_list_anchors(site,
                                           'site',
                                           site_language['ResFacetContributorsLabelTitle'],
                                           search_qs,
                                           site_language,
                                           query_dict)
    if dctype:
        facet_string += facet_list_anchors(dctype,
                                           'mt',
                                           site_language['ResFacetMediaTypesLabelTitle'],
                                           search_qs,
                                           site_language,
                                           query_dict)
    if fspatial:
        facet_string += facet_list_anchors(fspatial,
                                           'lc',
                                           site_language['ResFacetMapLabelTitle'],
                                           search_qs,
                                           site_language,
                                           query_dict)
    if fgroupname:
        facet_string += facet_list_anchors(fgroupname,
                                           'grn',
                                           site_language['ResFacetGroupsLabelTitle'],
                                           search_qs,
                                           site_language,
                                           query_dict)
    if item_type:
        facet_string += facet_list_anchors(item_type,
                                           'itype',
                                           site_language['ResFacetItemTypesLabelTitle'],
                                           search_qs,
                                           site_language,
                                           query_dict)

    if decades:
        facet_string += get_decades(facets, search_qs, site_language)

    # if featureComment
    if 'true' in feature_comment or 'true' in feature_mystery:
        facet_string += ('<fieldset>'
                         '<legend>%s</legend>'
                         '<ul class="options">'
                         % site_language['ResFacetFeaturesLabelTitle'])
        if 'true' in feature_comment:
            i = feature_comment.index('true')
            facet_string += ('<li>'
                             '%s%s&amp;fc=true">'
                             '<img src="%s" alt="comments" class="img-icon"/> &#160; '
                             '%s (%s)'
                             '</a>'
                             '</li>'
                             % (base_results_url,
                                search_qs,
                                type_icons('comment', 'icon'),
                                site_language['AdvLabelComment'],
                                str(feature_comment[i + 1])))
            # print 'Comments: '+str(featureComment[i+1])
        if 'true' in feature_mystery:
            i = feature_mystery.index('true')
            # print 'Mysteries: '+str(featureMystery[i+1])
            facet_string += ('<li>'
                             '%s%s&amp;fm=true">'
                             '<img src="%s" alt="mysteries" class="img-icon"/> '
                             '&#160; %s (%s)'
                             '</a>'
                             '</li>'
                             % (base_results_url,
                                search_qs,
                                type_icons('mystery', 'icon'),
                                site_language['AdvLabelMystery'],
                                str(feature_mystery[i + 1])))
        facet_string += '</ul></fieldset>'

    if rights_creative_commons:
        facet_string += facet_list_anchors(rights_creative_commons,
                                           'fcc',
                                           'Creative Commons',
                                           search_qs,
                                           site_language,
                                           query_dict)
    # print facetString
    facet_string += '</div>'
    return facet_string


def facet_list_anchors(list_name, portal_field, legend, search_qs, site_language, query_dict):
    anchors = ''
    sort_show = ''
    existing_query = ''
    # check for portal_field in query_dict
    if portal_field in query_dict:
        existing_query = query_dict[portal_field]
        # log_request('portal_field (utilities.395)', portal_field)
        # log_request('existing_query (utilities.396)', existing_query)
    open_fieldset = ('<fieldset id="%s"><legend>%s</legend><ul class="options" id="%s-sort">'
                     % (portal_field, legend, portal_field))
    close_list = '</ul>'
    close_fieldset = '</fieldset>'
    # TODO eliminate 'None (0)' as value ... shouldn't be coming from solr, but it is
    more_list = False
    end_anchor = '</a>'
    if len(list_name) > 10 and portal_field != 'mt' and portal_field != 'fcc':
        more_list = True
        # extra = (len(list_name)-6)/2
    suppress_anchor = False
    for i in range(len(list_name)):
        if i % 2 == 1:
            countli = str(list_name[i])
            if suppress_anchor is False:
                anchors += ' (<span title="%s">%s</span>)%s</li>' % (countli, countli, end_anchor)
            else:
                # reset suppress_anchor
                suppress_anchor = False
        else:
            value = str(list_name[i])
            re_value = value
            re_value = re_value.replace('\\', '\\\\')
            re_value = re_value.replace('(', '\\(')
            re_value = re_value.replace('?', '\\?')
            re_value = re_value.replace(')', '\\)')
            re_value = '\\b%s\\b' % re_value
            value_found = re.search(re_value, existing_query)
            # log_request('re_value (utilities.423)', re_value)
            # log_request('value_found (utilities.424)', value_found)
            if value_found:
                suppress_anchor = True
            if portal_field == 'mt':
                type_class = type_icons(list_name[i], 'class')
                list_class = '<li class="%s">' % type_class
                label = str(list_name[i]).title()
            elif portal_field == 'fcc':
                list_class = '<li>'
                cclabel = str(list_name[i]).title()
                label = '<img src="%s/img/%s.png" alt="%s" />' % (STATIC_URL, cclabel, cclabel)
            else:
                label = str(list_name[i])
                if i > 6:
                    list_class = '<li class="moreli">'
                else:
                    list_class = '<li>'
            if label == 'None' and portal_field == 'lc':
                original_label = label
                label = site_language['result_facet_location_unidentified']
                local_base_results_url = ''
                end_anchor = ''
            else:
                original_label = label
                local_base_results_url = base_results_url
                end_anchor = '</a>'
            # TODO set itemtype up as tagcloud with relative size logic
            if list_name[i + 1] > 0 and original_label != 'None' and label and suppress_anchor is False:
                anchors += ('%s%s%s&amp;%s=%s">%s'
                            % (list_class,
                               local_base_results_url,
                               search_qs,
                               portal_field,
                               parse.quote_plus(list_name[i]),
                               label))
            elif label and original_label != 'None':
                anchors += '%s<div class="facetFilterActive">%s</div></li>' % (list_class, label)
            else:
                suppress_anchor = True
    if more_list:
        sort_show = ('<div '
                     'id="%s-more">'
                     '%s ...</div>'
                     '<div id="%s-less">'
                     '%s ...</div>'
                     '<div id="%s-alpha">'
                     '%s...</div>'
                     '<div id="%s-numeric">%s...</div>'
                     % (portal_field,
                        site_language['results_see_more'],
                        portal_field,
                        site_language['results_see_less'],
                        portal_field,
                        site_language['results_sort_az'],
                        portal_field,
                        site_language['results_sort_91']))
    fieldset = open_fieldset + anchors + close_list + sort_show + close_fieldset
    return fieldset


def type_icons(dctype, response):
    # media specific calls, expect "response" value to be either 'icon' or 'class'
    dctype = dctype.lower()
    base_class = 'option-type-'
    icon_url = ''
    icon_class = ''
    if dctype == 'audio':
        icon = 'audio.png'
        icon_class = dctype
    elif dctype == 'collection':
        icon = 'collection.png'
        icon_class = dctype
    elif dctype == 'genealogical resource' or dctype == 'genealogicalresource':
        icon = 'genealogy.png'
        icon_class = 'genealogy'
    elif dctype == 'image':
        icon = 'image.png'
        icon_class = 'images'
    elif dctype == 'newspaper':
        icon = 'newspaper.png'
        icon_class = dctype
    elif dctype == 'object' or dctype == 'physical object' or dctype == 'physicalobject':
        icon = 'object.png'
        icon_class = dctype
    elif dctype == 'publication':
        icon = 'publication.png'
        icon_class = dctype
    elif dctype == 'text':
        icon = 'text.png'
        icon_class = dctype
    elif dctype == 'video':
        icon = 'video.png'
        icon_class = dctype
    elif dctype == 'website':
        icon = 'website.png'
        icon_class = dctype
    elif dctype == 'group':
        icon = 'group.png'
        icon_class = dctype
    elif dctype == 'exhibit':
        icon = 'exhibit.png'
        icon_class = dctype
    elif dctype == 'mystery':
        icon = 'mystery.png'
        icon_class = dctype
    elif dctype == 'comment':
        icon = 'comment.png'
        icon_class = dctype
    elif dctype == 'issue':
        icon = 'text.png'
        icon_class = dctype
    elif dctype == 'place':
        icon = 'place.png'
        icon_class = dctype
    elif dctype == 'organization':
        icon = 'organization.png'
        icon_class = dctype
    elif dctype == 'ship':
        icon = 'ship.png'
        icon_class = dctype
    elif dctype == 'ship document' or dctype == 'shipdocument':
        icon = 'shipdoc.png'
        icon_class = 'shipdocument'
    else:
        icon = ''
    if icon != '':
        icon_url = '%simg/%s' % (STATIC_URL, icon)
        icon_class = '%s%s' % (base_class, icon_class)
    if response == 'icon':
        return icon_url
    else:
        return icon_class


def get_decades(facets, search_qs, site_language):
    temp_decades = facets['fDateDecade'][::2]
    # print(temp_decades)
    decades = []
    for dec in temp_decades:
        if isinstance(dec, int):
            # we have an integer
            if dec < 1000:
                dec *= '0'
            if dec > 1500:
                decades.append(dec)
        else:
            # we have a string
            if dec.isdigit():
                dec_int = int(dec)
                if len(dec) == 3:
                    dec = '%s0' % dec
                    dec_int = dec_int * 10
                if dec_int > 1500:
                    decades.append(dec)
    # len_decades = len(decades)
    if len(decades) < 1:
        # if we can't process the decades then return an empty string
        return ""
    else:
        decade_row = ''
        temp_years = facets['fDateYear'][::2]
        # print(temp_years)
        years = []
        for yr in temp_years:
            if isinstance(yr, int):
                if yr > 1500:
                    years.append(yr)
            else:
                if yr.isdigit():
                    years.append(yr)
                else:
                    years.append("")
        # print(years)
        bottom_floor = decades[0]
        floor_i = int(bottom_floor)
        year = floor_i
        # look at last for string of 4 characters
        # if not, loop back to previous decade and repeat test
        # perhaps add test for extent beyond current decade ...
        ceiling_decade = int(decades[-1])
        this_decade = current_decade()
        if ceiling_decade > this_decade:
            ceiling_decade = this_decade
        header = ('<fieldset id="decadeTable">'
                  '<legend>%s</legend>'
                  '<div class="FacetPanelContent">'
                  '<table>'
                  % site_language['ResFacetYearsLabelTitle'])
        footer = '</table></div></fieldset>'
        while floor_i < (ceiling_decade + 1):
            floor_s = str(floor_i)
            floor_dd = str(int(floor_i / 10))
            decade_row += ('<tr>'
                           '<td class="decade">'
                           '<a href="results?dd=%s&amp;%s">'
                           '%s'
                           '</a>'
                           '</td>'
                           % (floor_dd, search_qs, floor_s))
            floor_i += 10
            # iterate through the decade
            while year < floor_i:
                if str(year) in years:
                    decade_row += ('<td class="year">'
                                   '<a href="results?dy=%s&amp;%s">'
                                   '%s'
                                   '</a>'
                                   '</td>'
                                   % (year, search_qs, year))
                else:
                    decade_row += '<td class="year">%s</td>' % year
                year += 1
            decade_row += '</tr>'
        facet_decades = '%s%s%s' % (header, decade_row, footer)
        return facet_decades


def get_media_label(mt, site_language):
    mt_upper = mt.upper()
    media_label = ''
    if mt_upper == 'IMAGE':
        media_label = site_language['AdvLabelMediaImage']
    elif mt_upper == 'TEXT':
        media_label = site_language['AdvLabelMediaText']
    elif mt_upper == 'AUDIO':
        media_label = site_language['AdvLabelMediaAudio']
    elif mt_upper == 'VIDEO':
        media_label = site_language['AdvLabelMediaVideo']
    elif mt_upper == 'WEBSITE':
        media_label = site_language['AdvLabelMediaWebsite']
    elif mt_upper == 'COLLECTION':
        media_label = site_language['AdvLabelMediaCollection']
    elif mt_upper == 'PHYSICALOBJECT' or mt_upper == 'OBJECT':
        media_label = site_language['AdvLabelMediaObject']
    elif mt_upper == 'GENEALOGICAL RESOURCE' or mt_upper == 'GENEALOGICALRESOURCE':
        media_label = site_language['AdvLabelMediaGenealogy']
    elif mt_upper == 'NEWSPAPER':
        media_label = site_language['AdvLabelMediaNewspapers']
    elif mt_upper == 'ORGANIZATION':
        media_label = site_language['AdvLabelMediaOrganization']
    elif mt_upper == 'PUBLICATION':
        media_label = site_language['AdvLabelMediaPublication']
    elif mt_upper == 'PLACE':
        media_label = site_language['AdvLabelMediaPlace']
    elif mt_upper == 'GROUP':
        media_label = site_language['AdvLabelMediaGroup']
    elif mt_upper == 'EXHIBIT':
        media_label = site_language['AdvLabelMediaExhibit']
    elif mt_upper == 'SHIP':
        media_label = site_language['AdvLabelMediaShip']
    elif mt_upper == 'SHIP DOCUMENT':
        media_label = site_language['AdvLabelMediaShipDocs']
    return media_label


def current_decade():
    current_year = str(datetime.now().year)
    decade = int(current_year[:3] + '0')
    return decade
