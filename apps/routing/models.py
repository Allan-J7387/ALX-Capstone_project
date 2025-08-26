from django.db import models
from django.conf import settings

class Route(models.Model):
    STATUS = [("PLANNED","Planned"),("DISPATCHED","Dispatched"),("IN_PROGRESS","In progress"),("COMPLETED","Completed"),("CANCELLED","Cancelled")]
    service_date = models.DateField()
    zone = models.ForeignKey("locations.Zone", on_delete=models.PROTECT)
    vehicle = models.ForeignKey("fleet.Vehicle", null=True, blank=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey("fleet.Driver", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS, default="PLANNED")
    total_distance_km = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RouteStop(models.Model):
    STATUS = [("PENDING","Pending"),("SKIPPED","Skipped"),("SERVED","Served")]
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    collection_request = models.ForeignKey("waste.CollectionRequest", null=True, blank=True, on_delete=models.SET_NULL)
    sequence = models.IntegerField(null=True, blank=True)
    eta = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
