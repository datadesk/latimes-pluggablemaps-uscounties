# Models
from django.contrib.gis.db import models

# Other helpers
from copy import deepcopy
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.models import USStateField
from django.contrib.gis.gdal import OGRGeometry, OGRGeomType


class County(models.Model):
    """
    An administrative unit dividing up an American state.
    
    Created by the U.S. Census Bureau's 2009 TIGER/Line project.
    
    Source: http://www2.census.gov/cgi-bin/shapefiles2009/national-files
    """
    # Description
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    state = USStateField(blank=True, null=True)
    square_miles = models.FloatField(null=True, blank=True)
    
    # ID codes
    state_fips_code = models.CharField(_('state FIPS code'), max_length=2)
    county_fips_code = models.CharField(_('county FIPS code'), max_length=3)
    fips_code = models.CharField(_('complete FIPS code'), max_length=5)
    county_ansi_code = models.CharField(_('county ANSI code'), max_length=8)
    csa_code = models.CharField(_('combined statistical area code'),
        max_length=3)
    msa_code = models.CharField(
        _('metropolitan/micropolitan statistical area code'), max_length=5)
    mda_code = models.CharField(_('metropolitan division code'), max_length=5)
    FUNCTIONAL_STATUS_CHOICES = ()
    functional_status = models.CharField(max_length=1)
    
    # Boundaries
    GEOM_FIELD_LIST = ( # We can use this list later in views to exclude 
                        # bulky geometry fields from database queries
        'polygon_4269', 'polygon_4326', 'polygon_900913',
        'simple_polygon_4269', 'simple_polygon_4326', 'simple_polygon_900913',
    )
    polygon_4269 = models.MultiPolygonField(_("Boundary"), srid=4269,
        null=True, blank=True)
    polygon_4326 = models.MultiPolygonField(srid=4326, null=True, blank=True)
    polygon_900913 = models.MultiPolygonField(srid=900913, null=True,
        blank=True)
    simple_polygon_4269 = models.MultiPolygonField(srid=4269, null=True,
        blank=True)
    simple_polygon_4326 = models.MultiPolygonField(srid=4326, null=True,
        blank=True)
    simple_polygon_900913 = models.MultiPolygonField(srid=900913, null=True, 
        blank=True)
    
    # Managers
    objects = models.GeoManager()
    
    class Meta:
        ordering = ('state', 'full_name',)
        verbose_name = 'U.S. county'
        verbose_name_plural = 'U.S. counties'
    
    def __unicode__(self):
        return u'%s, %s' % (self.full_name, self.state)
    
    def get_square_miles(self):
        """
        Returns the neighborhoods area in square miles.
        """
        if not self.polygon_4269:
            return False
        
        # Reproject the polygon from 4269, which is measured in 
        # decimal degrees to 3310, California Albers, which is measured 
        # in feet.
        copy = self.polygon_4269.transform(2229, clone=True)
        # square_meters = self.polygon_4269.area
        
        # One square foot equals 0.0929 square meters, 
        # so we can do the conversion like so
        # square_feet = square_meters / 0.0929
        square_feet = copy.area
        
        # There are 27,878,400 square feet in a square mile,
        # so we can do the conversion like so
        square_miles = square_feet / 27878400.0
        
        # Set the field and close out
        return square_miles
    
    #
    # Sync polygons
    #
    
    def get_srid_list(self):
        """
        Returns all of the SRIDs in the polygon set.
        """
        # Pull the meta data for the model
        opts = self.__class__._meta
        
        # Filter the field set down to the polygon fields
        fields = [i.name for i in opts.fields if i.name.startswith('polygon_')]
        
        # Return the SRID number that comes after the underscore.
        return [int(i.split('_')[1]) for i in fields]
    
    def set_polygons(self, canonical_srid=4269):
        """
        Syncs all polygon fields to the one true field, defined by the 
        `canonical_srid` parameter.
        
        Returns True if successful.
        """
        # Make sure it's a legit srid
        srid_list = self.get_srid_list()
        if canonical_srid not in srid_list:
            raise ValueError("canonical_srid must exist on the model.")
        
        # Grab the canonical data
        canonical_field = 'polygon_%s' % str(canonical_srid)
        canonical_data = getattr(self, canonical_field)
        
        # Update the rest of the fields
        srid_list.remove(canonical_srid)
        for srid in srid_list:
            this_field = 'polygon_%s' % str(srid)
            setattr(self, this_field, canonical_data)
        return True

    def set_simple_polygons(self, tolerance=500):
        """
        Simplifies the source polygons so they don't use so many points.
        
        Provide a tolerance score the indicates how sharply the
        the lines should be redrawn.
        
        Returns True if successful.
        """
        # Get the list of SRIDs we need to update
        srid_list = self.get_srid_list()
        
        # Loop through each
        for srid in srid_list:
            
            # Fetch the source polygon
            source_field_name = 'polygon_%s' % str(srid)
            source = getattr(self, source_field_name)
            
            # Fetch the target polygon where the result will be saved
            target_field_name = 'simple_%s' % source_field_name
            
            # If there's nothing to transform, drop out now.
            if not source:
                setattr(self, target_field_name, None)
                continue
            
            if srid != 900913:
                # Transform the source out of lng/lat before the simplification
                copy = source.transform(900913, clone=True)
            else:
                copy = deepcopy(source)
            
            # Simplify the source
            simple = copy.simplify(tolerance, True)
            
            # If the result is a polygon ...
            if simple.geom_type == 'Polygon':
                # Create a new Multipolygon shell
                mp = OGRGeometry(OGRGeomType('MultiPolygon'))
                # Transform the new poly back to its SRID
                simple.transform(srid)
                # Stuff it in the shell
                mp.add(simple.wkt)
                # Grab the WKT
                target = mp.wkt
            
            # If it's not a polygon...
            else:
                # It should be ready to go, so transform
                simple.transform(srid)
                # And grab the WKT
                target = simple.wkt
            
            # Stuff the WKT into the field
            setattr(self, target_field_name, target)
        return True



