from django.urls import path
from .views import *

urlpatterns = [
    path('map/', vessel_map, name='vessel_map'),
    path('ajax/list/', ajax_vessels_list, name='ajax_vessels_list')
]
