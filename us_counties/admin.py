# Admin
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

# Models
from us_counties.models import County


class CountyAdmin(OSMGeoAdmin):
    list_display = ('full_name', 'state')
    list_filter = ('state', 'functional_status')
    search_fields = ('full_name',)
    fieldsets = (
        (('Boundaries'),
            {'fields': ('polygon_4269', ),
             'classes': ('wide',),
            }
        ),
        (('Description'),
           {'fields': (
                'short_name', 'full_name', 'slug', 'state', 'square_miles',),
            'classes': ('wide',),
           }
        ),
        (('ID Codes'),
           {'fields': (
                'state_fips_code', 'county_fips_code', 'fips_code',
                'county_ansi_code', 'csa_code', 'msa_code', 'mda_code',
                'functional_status',),
            'classes': ('wide',),
           }
        ),
     )
    readonly_fields = (
        'full_name', 'short_name', 'slug', 'state', 'square_miles',
        'state_fips_code', 'county_fips_code', 'fips_code',
        'county_ansi_code', 'csa_code', 'msa_code', 'mda_code',
        'functional_status'
        )
    layerswitcher = False
    scrollable = False
    map_width = 400
    map_height = 400
    modifiable = False

admin.site.register(County, CountyAdmin)
