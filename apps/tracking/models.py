from django.db import models

class GPSLog(models.Model):
    route = models.ForeignKey("routing.Route", on_delete=models.CASCADE, related_name="gpslogs")
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.FloatField(null=True, blank=True)
