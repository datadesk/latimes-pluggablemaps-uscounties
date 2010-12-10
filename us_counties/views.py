# Response helpers
from django.http import Http404
from django.views.generic.simple import direct_to_template

# Models
from us_counties.models import County

# State abbrevations and such
from django.contrib.localflavor.us.us_states import STATE_CHOICES
STATE_DICT = {}
for x, y in STATE_CHOICES: STATE_DICT[x] = y


def state_detail(request, srid=900913, template='us_counties/openlayers.html',
    mimetype="text/html"):
    """
    A simple example of how you could make a map of all the counties in a state.
    """
    # Validate the state, falling back to California
    state = request.GET.get('state', 'CA') or 'CA'
    state_name = STATE_DICT.get(state, None)
    if not state_name:
        raise Http404
    # Prep a state list a pulldown menu
    state_list = [dict(slug=i[0], name=i[1]) for i in STATE_CHOICES]
    # Query the county list for the template
    object_list = County.objects.filter(state=state).only(
        'full_name', 'slug', 'simple_polygon_%s' % srid
        )
    return direct_to_template(request, template, locals(), mimetype=mimetype)


def state_detail_kml(request):
    response = state_detail(
        request,
        srid=4326,
        template='us_counties/county_list.kml',
        mimetype='application/vnd.google-earth.kml+xml',
    )
    # Set the filename for the response header
    filename = u'filename=state.kml'
    response['Content-Disposition'] = filename
    return response


