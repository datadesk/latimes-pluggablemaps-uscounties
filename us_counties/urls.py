from django.conf.urls.defaults import *

urlpatterns = patterns('us_counties.views',
    # Maps
    url(r'^openlayers/$', 'state_detail', {'template': 'us_counties/openlayers.html'},
        name='us_counties_openlayers'),
    url(r'^polymaps/$', 'state_detail', {'template': 'us_counties/polymaps.html'},
        name='us_counties_polymaps'),
    # Syndication
    url(r'^json/$', 'state_detail', {
        'srid': 4326,
        'format': 'json',
        'template': 'us_counties/county_list.json',
        }, name='us_counties_json'),
    url(r'^kml/$', 'state_detail', {
        'srid': 4326,
        'format': 'kml',
        'template': 'us_counties/county_list.kml',
    }, name='us_counties_kml'),
    url(r'^csv/$', 'state_detail', {
        'srid': 4326,
        'format': 'csv',
        'template': 'us_counties/county_list.csv',
    }, name='us_counties_csv'),
)

