#!/usr/bin/env python

from dateutil import parser
from datetime import datetime
from django.utils.timezone import make_aware

import django
import requests
import re
import os
import sys

# Set up Django
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.join (CURRENT_DIR, '..')
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ycm.settings'
django.setup()
# Django ready

from ycm.settings import AISHUB_API_KEY
from vessels.models import *

def get_kml_data(data, key):
    regex = r'<Data name="%s">.*?<value>(.*?)</value>' % key
    match = re.search(regex, data, re.S)
    if match:
        return match.group(1)
    else:
        return None

def get_position_report_from_garmin(boat_name):
    url = "https://share.garmin.com/Feed/Share/%s" % boat_name
    r = requests.get(url=url)
    if r.status_code != 200:
        return None

    data = r.content.decode('utf-8')
    if data == '':
        return None

    time = get_kml_data(data, 'Time UTC')
    time = parser.parse(time)
    time = make_aware(time)
    latitude = get_kml_data(data, 'Latitude')
    longitude = get_kml_data(data, 'Longitude')
    velocity = get_kml_data(data, 'Velocity').split()[0]
    velocity = float(velocity) * 0.539957 # Convert to knots
    course = get_kml_data(data, 'Course').split()[0]
    response = {
        'date': time,
        'latitude': latitude,
        'longitude': longitude,
        'speed': velocity,
        'heading': course
    }
    return response

def get_position_report_from_predictwind(boat_name):
    url = "https://forecast.predictwind.com/vodafone/%s.json" % boat_name
    r = requests.get(url=url)
    if r.status_code != 200:
        return None
    data = r.json()['route'][-1]
    response = {
            'date': make_aware(datetime.fromtimestamp(data['t'])),
            'latitude': data['p']['lat'],
            'longitude': data['p']['lon'],
            'speed': 0,
            'heading': data['bearing']
    }
    return response

def get_position_reports_from_aishub():
    if AISHUB_API_KEY is None:
        return False

    mmsi_list = Vessel.objects.values_list('mmsi', flat=True)

    if len(mmsi_list) == 0:
        return False

    response = requests.get('https://data.aishub.net/ws.php', {
        'username': AISHUB_API_KEY,    # Requires an API key
        'format': 1,
        'output': 'json',
        'compress': 0,
        'mmsi': mmsi_list
    })
    try:
        data = response.json()
    except ValueError:
        return False
    if data[0]['ERROR'] == True:
        return False
    for entry in data[1]:
        mmsi = entry['MMSI']
        try:
            vessel = Vessel.objects.get(mmsi=mmsi)
        except Vessel.DoesNotExist:
            continue
        vessel.longitude = entry['LONGITUDE']
        vessel.latitude = entry['LATITUDE']
        vessel.heading = entry['HEADING']
        vessel.speed = entry['SOG']
        vessel.boat_type = entry['TYPE']
        vessel.position_received_on = parser.parse(entry['TIME'])
        vessel.save()

def refresh_vessel_positions():
    objects = VesselPositionsLastRetrieved.objects.all()
    if objects.count() == 0:
        new_object = VesselPositionsLastRetrieved()
        new_object.save()
    else:
        # Do not poll the API more often than every N minutes
        if objects[0].seconds_ago(1*60) == False:
            return False

    vessels = Vessel.objects.exclude(tracking_url='').exclude(tracking_url=None).all()
    for vessel in vessels:
        regex = r'https://forecast.predictwind.com/tracking/display/([^/]+)/'
        match = re.search(regex, vessel.tracking_url)
        if match:
            boat_name = match.group(1)
            data = get_position_report_from_predictwind(boat_name)
            if data is not None:
                vessel.position_received_on = data['date']
                vessel.latitude = data['latitude']
                vessel.longitude = data['longitude']
                vessel.speed = data['speed']
                vessel.heading = data['heading']
                vessel.save()
            continue

        regex = r'https://share.garmin.com/([a-zA-Z0-9]+)'
        match = re.search(regex, vessel.tracking_url)
        if match:
            boat_name = match.group(1)
            data = get_position_report_from_garmin(boat_name)
            if data is not None:
                vessel.position_received_on = data['date']
                vessel.latitude = data['latitude']
                vessel.longitude = data['longitude']
                vessel.speed = data['speed']
                vessel.heading = data['heading']
                vessel.save()
            continue

    # Get the remaining position reports from AIS 
    get_position_reports_from_aishub()
     
    # Update the timestamp so we don't query the API too often
    objects[0].save()
    return True

if __name__ == "__main__":
   refresh_vessel_positions() 
