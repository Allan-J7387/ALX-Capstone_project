from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = [
        ("INFO", "Information"),
        ("WARNING", "Warning"),
        ("ERROR", "Error"),
        ("SUCCESS", "Success")
    ]
    CHANNELS = [("EMAIL","Email"),("SMS","SMS"),("PUSH","Push")]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="INFO")
    channel = models.CharField(max_length=10, choices=CHANNELS, default="EMAIL")
    title = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type}: {self.message[:50]}..."
