from django.conf.urls.defaults import *

urlpatterns = patterns('us_counties.views',
    url(r'^openlayers/$', 'state_detail', {'template': 'us_counties/openlayers.html'},
        name='us_counties_openlayers'),
    url(r'^polymaps/$', 'state_detail', {'template': 'us_counties/polymaps.html'},
        name='us_counties_polymaps'),
    url(r'^json/$', 'state_detail', {
        'srid': 4326,
        'template': 'us_counties/county_list.json',
        'mimetype': 'text/javascript',
        }, name='us_counties_json'),
    url(r'^kml/$', 'state_detail', {
        'srid': 4326,
        'template': 'us_counties/county_list.kml',
        'mimetype': 'application/vnd.google-earth.kml+xml',
    }, name='us_counties_kml'),
)

