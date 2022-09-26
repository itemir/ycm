from django.urls import path
from .views import *

urlpatterns = [
    path('<int:member_id>/', member_detail, name='member_detail'),
    path('list/', list_members, name='list_members'),
    path('update/', update_member, name='update_member'),
]
