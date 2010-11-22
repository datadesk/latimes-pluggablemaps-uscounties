from django.conf.urls.defaults import *

urlpatterns = patterns('us_counties.views',
    url(r'^openlayers/$', 'state_detail', {'template': 'openlayers.html'},
        name='us_counties_openlayers'),
    #url(r'^polymaps/$', 'state_detail', {'template': 'polymaps.html'},
    #    name='us_counties_polymaps'),
    #url(r'^json/$', 'json', name='us_counties_json'),
    #url(r'^raphael/$', 'raphael', name='us_counties-raphael'),
)

