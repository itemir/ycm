from django.urls import path
from .views import *

urlpatterns = [
    path('list/', list_members, name='list_members'),
    path('update/', update_member, name='update_member'),
]
