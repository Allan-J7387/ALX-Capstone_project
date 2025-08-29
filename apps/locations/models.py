from django.db import models
from django.conf import settings

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="addresses")
    label = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.street}, {self.city}"

class Zone(models.Model):
    name = models.CharField(max_length=100)
    polygon_geojson = models.TextField(blank=True)  # store geojson for boundaries

    def __str__(self):
        return self.name
