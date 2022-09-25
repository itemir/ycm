from django.db import models
from django.utils import timezone
from datetime import timedelta

class VesselPositionsLastRetrieved(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    def seconds_ago(self, limit):
        now = timezone.now()
        if now - self.last_updated >= timedelta(seconds=limit):
            return True
        else:
            return False

class Vessel(models.Model):
    name = models.CharField(max_length=100, db_index=True, null=True)
    tracking_url = models.CharField(max_length=255, null=True, blank=True)
    mmsi = models.BigIntegerField(null=True, blank=True)
    position_received_on = models.DateTimeField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    boat_type = models.IntegerField(null=True, blank=True)
    heading = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['name', 'mmsi']
    def __str__(self):
        if self is None:
            return ''
        elif self.name is None:
            return ''
        else:
            return self.name
