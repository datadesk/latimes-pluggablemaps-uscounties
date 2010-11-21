from django.conf.urls.defaults import *

urlpatterns = patterns('us_counties.views',
    url(r'^openlayers/$', 'state_detail', {'template': 'openlayers.html'},
        name='us_counties-openlayers'),
    #url(r'^polymaps/$', 'polymaps', name='us_counties-polymaps'),
    #url(r'^raphael/$', 'raphael', name='us_counties-raphael'),
)

