from django.db import models
from django.conf import settings

class Notification(models.Model):
    CHANNELS = [("EMAIL","Email"),("SMS","SMS"),("PUSH","Push")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    channel = models.CharField(max_length=10, choices=CHANNELS, default="EMAIL")
    title = models.CharField(max_length=255)
    body = models.TextField()
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
