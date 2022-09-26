from django.shortcuts import render, get_object_or_404, reverse
from vessels.models import *
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

@login_required
def vessel_detail(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id)
    return render(request, 'vessels/detail.html', {
        'vessel': vessel
    })

@login_required
def vessel_map(request):
    return render(request, 'vessels/map.html')

@login_required
def list_vessels(request):
    vessels = Vessel.objects.all()
    return render(request, 'vessels/list.html', {
        'vessels': vessels
    })

@login_required
def ajax_vessels_list(request):
    vessels = Vessel.objects.all()
    vessels = vessels.exclude(position_received_on=None)
    vessels = vessels.exclude(privacy_mode=True)
    vessel_list = []
    for vessel in vessels:
        vessel_list.append({
            'name': vessel.name,
            'url': reverse('vessel_detail', kwargs={'vessel_id': vessel.id}), 
            'make_and_model': vessel.make_and_model,
            'year_built': vessel.year_built,
            'latitude': vessel.latitude,
            'longitude': vessel.longitude,
            'speed': vessel.speed,
            'heading': vessel.heading,
            'ts': int(vessel.position_received_on.timestamp()*1000)
        })
    return JsonResponse(vessel_list, safe=False)
