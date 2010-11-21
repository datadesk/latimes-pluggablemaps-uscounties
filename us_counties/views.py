from django.http import HttpResponse
from us_counties.models import County
from django.views.generic.simple import direct_to_template


def openlayers(request):
    state = request.GET.get('state', 'CA')
    object_list = County.objects.filter(state=state).only(
        'full_name', 'slug', 'simple_polygon_900913'
        )
    template = 'openlayers.html'
    return direct_to_template(request, template, locals())


def polymaps(request):
    return HttpResponse("OK")


def raphael(request):
    return HttpResponse("OK")
