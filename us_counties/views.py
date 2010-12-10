# Response helpers
from django.http import Http404
from django.views.generic.simple import direct_to_template

# Models
from us_counties.models import County

# State abbrevations and such
from django.contrib.localflavor.us.us_states import STATE_CHOICES
STATE_DICT = {}
for x, y in STATE_CHOICES: STATE_DICT[x] = y

MIMETYPES = {
    'kml': 'application/vnd.google-earth.kml+xml',
    'kmz': 'application/vnd.google-earth.kmz',
    'json': 'application/javascript',
    'csv': 'text/csv',
    'html': 'text/html',
}


def state_detail(request, template, srid=900913, format='html'):
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
    response = direct_to_template(request, template, locals(), mimetype=MIMETYPES[format])
    # Force a download to the specified filename, if there is one.
    if format != 'html':
        filename = u'filename=%s.%s' % (state_name.lower(), format)
        response['Content-Disposition'] = filename
    return response

