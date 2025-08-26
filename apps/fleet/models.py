from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    plate_number = models.CharField(max_length=32, unique=True)
    capacity_kg = models.IntegerField()
    STATUS = [("AVAILABLE","Available"),("IN_SERVICE","In service"),("MAINTENANCE","Maintenance")]
    status = models.CharField(max_length=20, choices=STATUS, default="AVAILABLE")
    current_zone = models.ForeignKey("locations.Zone", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.plate_number

class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=64, blank=True)
    assigned_vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} - Driver"
