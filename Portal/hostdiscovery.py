__author__ = 'walter'

from django.http import HttpRequest
from ODWPortal.models import Site, SiteSetup, Language


def site_host(request):
    site_dict = {}
    host = HttpRequest.build_absolute_uri(request)
    #print(host)
    sites = Site.objects.order_by('-site_url')
    #print(sites)
    for site in sites:
        if host.startswith(site.site_url):
            site_dict['site_id'] = site.id
            site_dict['site_name'] = site.site_name
            site_dict['site_url'] = site.site_url
            site_dict['language'] = site.language
            break
        else:
            # need a default to redirect to if the url isn't entered yet
            one = 1
    return site_dict


def site_settings(request):
    site_dict = site_host(request)
    site_id = site_dict['site_id']
    site_values = SiteSetup.objects.filter(site_id=site_id)
    for f in site_values:
        #print("function settings: " + f.afield + ":" + f.avalue)
        site_dict[f.afield] = f.avalue
    #print(site_dict)
    return site_dict


def site_language(language):
    site_lang = {}
    site_lang_rs = Language.objects.filter(site_language=language)
    for f in site_lang_rs:
        site_lang[f.afield] = f.avalue
    return site_lang