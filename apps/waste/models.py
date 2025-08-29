from django.db import models
from django.conf import settings

class CollectionRequest(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="requests/", null=True, blank=True)
    location_text = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

class WasteType(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CollectionRequest(models.Model):
    STATUS = [
        ("PENDING", "Pending"),
        ("SCHEDULED", "Scheduled"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="collection_requests")
    address = models.ForeignKey("locations.Address", on_delete=models.PROTECT)
    waste_type = models.ForeignKey(WasteType, on_delete=models.SET_NULL, null=True)
    quantity_kg = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    time_window_start = models.TimeField(null=True, blank=True)
    time_window_end = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    photo = models.ImageField(upload_to="requests/photos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Request #{self.id} by {self.requester}"

class RecurrenceSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey("locations.Address", on_delete=models.CASCADE)
    waste_type = models.ForeignKey(WasteType, on_delete=models.SET_NULL, null=True)
    day_of_week = models.IntegerField()  # 0=Monday ... 6=Sunday
    time_window_start = models.TimeField(null=True, blank=True)
    time_window_end = models.TimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

class IssueReport(models.Model):
    ISSUE_TYPE = [
        ("MISSED_PICKUP", "Missed pickup"),
        ("OVERFLOW", "Overflow"),
        ("OTHER", "Other"),
    ]
    STATUS = [("OPEN", "Open"), ("ACKNOWLEDGED", "Acknowledged"), ("RESOLVED", "Resolved")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey("locations.Address", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=ISSUE_TYPE)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="issues/photos/", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="OPEN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
