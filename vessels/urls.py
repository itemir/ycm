from django.urls import path
from .views import *

urlpatterns = [
    path('<int:vessel_id>/', vessel_detail, name='vessel_detail'),
    path('list/', list_vessels, name='list_vessels'),
    path('map/', vessel_map, name='vessel_map'),
    path('ajax/list/', ajax_vessels_list, name='ajax_vessels_list')
]
