from django.contrib import admin
from .models import Vehicle, Driver

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'capacity_kg', 'status', 'current_zone')
    list_filter = ('status', 'current_zone')
    search_fields = ('plate_number',)
    ordering = ('plate_number',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'assigned_vehicle')
    list_filter = ('assigned_vehicle__status',)
    search_fields = ('user__username', 'user__email', 'license_number')
    ordering = ('user__username',)
