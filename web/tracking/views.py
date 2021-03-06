import json

from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_datetime
import pytz

from django.db.models import Avg, Min, Max, Count

from tracking.models import Location
from tracking.models import Waypoints
from tracking.models import Position
from vehicles.models import Vehicle


def get_waypoints(vehicle_id=-1, from_date='1970-01-01', to_date='9999-12-31', from_time='00:00:00', to_time='23:59:59'):
    range_start = from_date + ' ' + from_time
    range_end   = to_date + ' ' + to_time
    Waypoints.set_time_utc(range_start, range_end)
    if vehicle_id == -1:
        return Waypoints.objects.all()
    else:
        return Waypoints.objects.filter(wp_vehicle_id=vehicle_id)
    

def get_position(vehicle_id=-1, at_date='9999-12-31', at_time='23:59:59'):
    Position.set_time_utc(at_date + ' ' + at_time)
    if vehicle_id == -1:
        return Position.objects.all()
    else:
        return Position.objects.filter(wp_vehicle_id=vehicle_id)

        
def get_latest_location(vehicle_vin='-1'):
    print vehicle_vin
    if vehicle_vin == '-1':
        return Location.objects.latest('loc_time').to_json()
    else:
        return Location.objects.filter(loc_vehicle__veh_vin=vehicle_vin).latest('loc_time').to_json()




def tracking(request, vehicle_id=-1, from_date='1970-01-01', to_date='9999-12-31', from_time='00:00:00', to_time='23:59:59'):
    template = loader.get_template('tracking/tracking.html')
    
    waypoints = get_waypoints(vehicle_id, from_date, to_date, from_time, to_time)

    context = RequestContext(request, {
        'waypoints': waypoints,
    })

    return HttpResponse(template.render(context))



def replay(request, vehicle_id=-1, from_date='1970-01-01', to_date='9999-12-31', from_time='00:00:00', to_time='23:59:59'):
    template = loader.get_template('tracking/replay.html')
    
    waypoints = get_waypoints(vehicle_id, from_date, to_date, from_time, to_time)
    
    context = RequestContext(request, {
        'waypoints': waypoints,
    })

    return HttpResponse(template.render(context))



def location(request, vehicle_id=-1, at_date='9999-12-31', at_time='23:59:59'):
    template = loader.get_template('tracking/location.html')
    
    position = get_position(vehicle_id, at_date, at_time)

    print 'vehicle: ', vehicle_id, "date: ", at_date, "time: ", at_time, "position: ", position

    context = RequestContext(request, {
        'position': position,
    })
    
    print 'Rendering tracking/location.html'
    return HttpResponse(template.render(context))


def latest_location(request, vehicle_id='-1'):

    location = get_latest_location(vehicle_id)

    print 'vehicle: ', vehicle_id, "latest location: ", location
    response_data = location;

    #return JsonResponse({'foo':'bar'})

    #return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(response_data, content_type="application/json")


def index(request):
    template = loader.get_template('tracking/index.html')
    
    maps = [{'id':'location','name':'Location'},{'id':'tracking','name':'Tracking'},{'id':'replay','name':'Replay'}]
    vehicles = Vehicle.objects.all()
    
    context = RequestContext(request, {
        'title' : 'Tracking',
        'maps': maps,
        'vehicles': vehicles,
    })
    
    print 'Rendering tracking/index.html'
    return HttpResponse(template.render(context))



def realtime(request, vehicle_id=-1):
    template = loader.get_template('tracking/realtime.html')
    
    waypoints = get_waypoints(vehicle_id)
    
    context = RequestContext(request, {
        'waypoints': waypoints,
    })

    return HttpResponse(template.render(context))


def test(request):
    template = loader.get_template('tracking/test.html')
    
    context = RequestContext(request, {
    })

    return HttpResponse(template.render(context))



