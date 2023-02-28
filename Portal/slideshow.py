from django.db import connections
from ODWPortal.models import Site, SiteSetup

def get_slideshow(request):
    slide_ul = ''
    agency_sql = "SELECT agency_id FROM view_portal_new_images_agency ORDER BY date_made_public DESC LIMIT 16;"
    agencies = sql_call(agency_sql)
    for agency in agencies:
        agency_id = agency[0]
        slide_sql = "SELECT R.title, comp_url, CONCAT(A.agency_image_url, RO.location,RO.file_name) AS comp_reg FROM records R JOIN agencies A ON R.agency_id = A.id JOIN recordobjects RO ON R.id = RO.record_id WHERE R.agency_id = '%s' AND RO.record_object_category_id_2 = '1' AND R.media_type_id = '1' AND public_display='1' AND date_made_public IS NOT NULL ORDER BY date_made_public DESC LIMIT 1;" % agency_id
        # print(slide_sql)
        slides = sql_call(slide_sql)
        for slide in slides:
            slide_title = slide[0].strip()
            slide_title = slide_title.replace('"', '&quot;')
            slide_url = slide[1].strip()
            slide_reg = slide[2].strip()
            slide_list = '<li><a href="%s" target="_blank"><img src="%s" alt="%s" title="%s" /></a></li>' % (slide_url, slide_reg, slide_title, slide_title)
            slide_ul += slide_list
    print(slide_ul)
    sites = Site.objects.all()
    for site in sites:
        site_id = site.id
        # print(site_id)
        afield = 'search_content_block_li'
        avalue = slide_ul
        try:
            existing_list = SiteSetup.objects.get(site_id=site_id, afield=afield)
        except SiteSetup.DoesNotExist:
            existing_list = None
        # print(existing_list)
        if existing_list:
            existing_list.avalue = avalue
            existing_list.save()
        else:
            s = SiteSetup(site_id=site_id, afield=afield, avalue=avalue)
            s.save()
    return "Done"


def sql_call(qry):
    with connections['vita'].cursor() as cur:
        cur.execute(qry)
        sqlrtn = cur.fetchall()
    cur.close()
    return sqlrtn