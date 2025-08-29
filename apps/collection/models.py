from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid
from apps.locations.serializers import AddressSerializer

User = settings.AUTH_USER_MODEL

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    label = models.CharField(max_length=255, blank=True)  # "Home", "Office"
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=32, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label or self.line1}, {self.city}"

class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('active','active'),
        ('maintenance','maintenance'),
        ('inactive','inactive'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plate_number = models.CharField(max_length=64, unique=True)
    model = models.CharField(max_length=128, blank=True)
    capacity_kg = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.plate_number}"

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    phone = models.CharField(max_length=32, blank=True)
    license_number = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

class PickupRequest(models.Model):
    STATUS_CHOICES = (
        ('requested','requested'),
        ('scheduled','scheduled'),
        ('in_progress','in_progress'),
        ('completed','completed'),
        ('cancelled','cancelled'),
        ('failed','failed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, related_name='pickup_requests', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='pickup_requests')
    scheduled_time = models.DateTimeField()
    items_description = models.TextField(blank=True)
    estimated_weight_kg = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='requested')
    assigned_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_pickups')
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_pickups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-scheduled_time', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_time']),
        ]

    def __str__(self):
        return f"Pickup {self.id} for {self.customer}"

class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='routes')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='routes')
    created_at = models.DateTimeField(auto_now_add=True)

class RouteStop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    pickup = models.ForeignKey(PickupRequest, on_delete=models.SET_NULL, null=True, blank=True)
    sequence = models.IntegerField(default=0)
    eta = models.DateTimeField(null=True, blank=True)

from django.db import models
from apps.locations.models import Address

class CollectionRequest(models.Model):
    waste_type = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="collection_requests")
    scheduled_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[("pending", "Pending"), ("in_progress", "In Progress"), ("completed", "Completed")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.waste_type} - {self.status}"
