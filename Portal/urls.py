from django.conf.urls import url

from django.contrib import admin
admin.autodiscover()
from Portal import views as portal_views


urlpatterns = [
    url(r'^(?i)$', portal_views.index, name='index'),
    #TODO 301 the 'search' page to start page; redirect to preferred url
    url(r'^(?i)search$', portal_views.index, name='index'),
    url(r'^(?i)advsearch$', portal_views.advsearch, name='advsearch'),
    url(r'^(?i)about', portal_views.about, name='about'),
    url(r'^(?i)help', portal_views.help_request, name='help_request'),
    url(r'^(?i)contributors', portal_views.contributors, name='contributors'),
    url(r'^(?i)results', portal_views.results, name='results'),
    url(r'^(?i)media', portal_views.mediatype, name='mediatype'),

    url(r'^(?i)rechercher', portal_views.index, name='index'),
    url(r'^(?i)apropos', portal_views.about, name='about'),
    url(r'^(?i)aide', portal_views.help_request, name='help_request'),
    url(r'^(?i)collaborateurs', portal_views.contributors, name='contributors'),
    url(r'^(?i)resultat', portal_views.results, name='results'),
    url(r'^(?i)mediatype', portal_views.mediatype, name='mediatype'),

    url(r'^(?i)dc', portal_views.xml, {"xml_type": "dc"}, name='dc'),
    url(r'^(?i)mods', portal_views.xml, {"xml_type": "mods"}, name='mods'),
    url(r'^(?i)json', portal_views.json_handler, name='json_handler'),

    url(r'^(?i)count', portal_views.count, name='count'),
    url(r'^(?i)slideshow', portal_views.slideshow, name='slideshow'),

    url(r'^(?i)admin/', admin.site.urls),
]
