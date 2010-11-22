# Response helpers
from django.http import Http404
from django.views.generic.simple import direct_to_template

# Models
from us_counties.models import County

# State abbrevations and such
from django.contrib.localflavor.us.us_states import STATE_CHOICES
STATE_DICT = {}
for x, y in STATE_CHOICES: STATE_DICT[x] = y


def state_detail(request, template='openlayers.html'):
    """
    A simple example of how you could make a map of all the counties in a state.
    """
    state = request.GET.get('state', 'CA') or 'CA'
    state_name = STATE_DICT.get(state, None)
    if not state_name:
        raise Http404
    state_list = [dict(slug=i[0], name=i[1]) for i in STATE_CHOICES]
    object_list = County.objects.filter(state=state).only(
        'full_name', 'slug', 'simple_polygon_900913'
        )
    return direct_to_template(request, template, locals())


def json(request):
    state = request.GET.get('state', None)
    if not state:
        raise Http404
    object_list = County.objects.filter(state=state).only(
        'full_name', 'slug', 'simple_polygon_4269'
        )
    return direct_to_template(request, 'county_list.json', locals(), 'text/javascript')


