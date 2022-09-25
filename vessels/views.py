from django.shortcuts import render
from vessels.models import *
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

@login_required
def vessel_map(request):
    return render(request, 'vessels/vessels_on_map.html')

@login_required
def ajax_vessels_list(request):
    vessels = Vessel.objects.exclude(position_received_on=None).all()
    vessel_list = []
    for vessel in vessels:
        vessel_list.append({
            'name': vessel.name,
            'latitude': vessel.latitude,
            'longitude': vessel.longitude,
            'speed': vessel.speed,
            'heading': vessel.heading,
            'ts': int(vessel.position_received_on.timestamp()*1000)
        })
    return JsonResponse(vessel_list, safe=False)
