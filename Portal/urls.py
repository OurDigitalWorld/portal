from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^(?i)$', 'Portal.views.index', name='index'),
     #TODO 301 the 'search' page to start page; redirect to preferred url
     url(r'^(?i)search$', 'Portal.views.index', name='index'),
     url(r'^(?i)advsearch$', 'Portal.views.advsearch', name='advsearch'),
     url(r'^(?i)about', 'Portal.views.about', name='about'),
     url(r'^(?i)faq', 'Portal.views.faq', name='faq'),
     url(r'^(?i)help', 'Portal.views.help_request', name='help_request'),
     url(r'^(?i)kml', 'Portal.views.kml', name='kml'),
     url(r'^(?i)features', 'Portal.views.features', name='features'),
     url(r'^(?i)contributors', 'Portal.views.contributors', name='contributors'),
     url(r'^(?i)searchwidgets', 'Portal.views.searchwidgets', name='searchwidgets'),
     url(r'^(?i)searchwidget.html', 'Portal.views.searchwidget', name='searchwidget'),
     url(r'^(?i)resultsXML', 'Portal.views.results_xml', name='results2'),
     #TODO 301 the 'resultXML' page to start page; redirect to preferred url
     url(r'^(?i)resultXML', 'Portal.views.results_xml', name='results2'),
     url(r'^(?i)results', 'Portal.views.results', {"result_type": "single"}, name='results'),
     url(r'^(?i)resultm', 'Portal.views.results', {"result_type": "multipane"}, name='results'),
     url(r'^(?i)dc', 'Portal.views.xml', {"xml_type": "dc"}, name='dc'),
     url(r'^(?i)mods', 'Portal.views.xml', {"xml_type": "mods"}, name='mods'),
     url(r'^(?i)rss', 'Portal.views.xml', {"xml_type": "rss"}, name='rss'),
     url(r'^(?i)atom', 'Portal.views.xml', {"xml_type": "atom"}, name='atom'),
     url(r'^(?i)rdf', 'Portal.views.xml', {"xml_type": "rdf"}, name='rdf'),
     url(r'^(?i)solr', 'Portal.views.xml', {"xml_type": "solr"}, name='solr'),
     url(r'^(?i).*\.kml', 'Portal.views.xml', {"xml_type": "kml"}, name='kml'),
     url(r'^(?i)json', 'Portal.views.json_handler', name='json_handler'),
     url(r'^(?i)mediatype', 'Portal.views.mediatype', name='mediatype'),
     url(r'^(?i)opensearch\.xml', 'Portal.views.opensearch', name='opensearch'),
     url(r'^(?i)rechercher', 'Portal.views.index', name='index'),
     url(r'^(?i)apropos', 'Portal.views.about', name='about'),
     url(r'^(?i)foire', 'Portal.views.faq', name='faq'),
     url(r'^(?i)aide', 'Portal.views.help_request', name='help_request'),
     url(r'^(?i)collaborateurs', 'Portal.views.contributors', name='contributors'),
     url(r'^(?i)media', 'Portal.views.mediatype', name='mediatype'),
     url(r'^(?i)gadgetlogiciel.html', 'Portal.views.searchwidget', name='searchwidget'),
     url(r'^(?i)resultat', 'Portal.views.results', name='results'),
     url(r'^(?i)count', 'Portal.views.count', name='count'),
     url(r'^(?i)unapi', 'Portal.views.unapi', name='unapi'),

     url(r'^(?i)admin/', include(admin.site.urls)),
)