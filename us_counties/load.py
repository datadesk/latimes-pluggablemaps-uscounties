"""
Utilities for loading boundaries into our Geodjango database.
"""
import gc
import os
import urllib
import zipfile
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

# The location of this directory
this_dir = os.path.dirname(__file__)
data_dir = os.path.join(this_dir, 'data')
# The location of our source files.
shp_file = os.path.join(data_dir, 'tl_2009_us_county.shp')
fips_file = os.path.join(data_dir, 'fips.csv')


def all():
    """
    Wrap it all together and load everything
    
    Example usage:
        
        >> from us_counties import load; load.all()

    """
    from models import County
    download()
    [i.delete() for i in County.objects.all()]
    shp()
    extras()


def download():
    """
    Download the shp files we will use as fodder
    
    Example usage:
    
        >> from us_counties import load; load.download();
    
    """
    # Download the zip
    target = 'https://github.com/downloads/datadesk/latimes-pluggablemaps-uscounties/tl_2009_us_county.zip'
    destination = os.path.join(data_dir, 'tl_2009_us_county.zip')
    urllib.urlretrieve(target, destination)
    # Unzip it
    fh = open(destination, 'rb')
    zfile = zipfile.ZipFile(fh)
    for name in zfile.namelist():
        path = os.path.join(data_dir, name)
        out = open(path, 'wb')
        out.write(zfile.read(name))
        out.close()
    fh.close()


def shp():
    """
    Load the ESRI shapefile from the Census in the County model.
    
    Example usage:
    
        >> from us_counties import load; load.shp();
    
    """
    # Import the database model where we want to store the data
    from models import County
    
    # A crosswalk between the fields in our database and the fields in our
    # source shapefile
    shp2db = {
        'polygon_4269': 'Polygon',
        'state_fips_code': 'STATEFP',
        'county_fips_code': 'COUNTYFP',
        'fips_code': 'CNTYIDFP',
        'county_ansi_code': 'COUNTYNS',
        'short_name': 'NAME',
        'full_name': 'NAMELSAD',
        'csa_code': 'CSAFP',
        'msa_code': 'CBSAFP',
        'mda_code': 'METDIVFP',
        'functional_status': 'FUNCSTAT',
    }
    # Load our model, shape, and the map between them into GeoDjango's magic
    # shape loading function (I also slipped the source coordinate system in
    # there. The Census says they put everything in NAD 83, which translates
    # to 4269 in the SRID id system.)
    lm = LayerMapping(County, shp_file, shp2db, source_srs=4269, encoding='latin-1')
    # Fire away!
    lm.save(verbose=False)


def abbrevs():
    """
    Load the postal abbreviations using the FIPS codes as our guide.
    """
    import csv
    from models import County
    f = open(fips_file, 'r')
    r = csv.DictReader(f, delimiter='\t')
    d = {}
    for i in r:
        d[i.get('FIPS')] = i.get('Abbreviation')
    return d


def extras():
    """
    Load some of the extra data we want for our model that's not included
    in the source shapefile. 
        
        * The Django state field
        * The slug field
        * The ForeignKey connection to a State model.
        * Simplified versions of our polygons that contain few points
        
    Example usage:
    
        >> from us_counties import load; load.extras();
        
    """
    from django.template.defaultfilters import slugify
    from models import County
    # Pull a crosswalk between FIPS and state abbreviations
    adict = abbrevs()
    # Loop through everybody...
    for obj in queryset_iterator(County.objects.all()):
        # ...set the state...
        obj.state = adict[obj.state_fips_code]
        # ...slug...
        obj.slug = u'%s-%s' % (slugify(obj.full_name), slugify(obj.state))
        # .. the full set of polygons...
        obj.set_polygons()
        # ... the square miles ...
        obj.square_miles = obj.get_square_miles()
        # ... save the changes ...
        obj.save()
    # ... and then loop again to set the simple polygons to avoid a weird bug
    # I've had when I do them right after the polygons.
    for obj in queryset_iterator(County.objects.all()):
        obj.set_simple_polygons()
        obj.save()


def queryset_iterator(queryset, chunksize=100):
    """
    Iterate over a Django Queryset ordered by the primary key
    
    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    
    Note that the implementation of the iterator does not support ordered query sets.
    
    Lifted from: http://www.mellowmorning.com/2010/03/03/django-query-set-iterator-for-really-large-querysets/
    """
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def specs():
    """
    Examine our source shapefile and print out some basic data about it.
    
    We can use this to draft the model where we store it in our system.
    
    Done according to documentation here: http://geodjango.org/docs/layermapping.html
    
    Example usage:
    
        >> from us_counties import load; load.specs();
    
    What we get in this case:
    
        Fields: ['STATEFP', 'COUNTYFP', 'COUNTYNS', 'CNTYIDFP', 'NAME',
                 'NAMELSAD', 'LSAD', 'CLASSFP', 'MTFCC', 'CSAFP', 'CBSAFP',
                 'METDIVFP', 'FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON']
        Number of features: 3234
        Geometry Type: Polygon
        SRS: GEOGCS["GCS_North_American_1983",
            DATUM["North_American_Datum_1983",
            SPHEROID["GRS_1980",6378137,298.257222101]],
        PRIMEM["Greenwich",0],
        UNIT["Degree",0.017453292519943295]]
    """
    # Crack open the shapefile
    ds = DataSource(shp_file)
    # Access the data layer
    layer = ds[0]
    # Print out all kinds of goodies
    print "Fields: %s" % layer.fields
    print "Number of features: %s" % len(layer)
    print "Geometry Type: %s" % layer.geom_type
    print "SRS: %s" % layer.srs


