from django.contrib import admin
from .models import Address, Vehicle, Driver, PickupRequest, Route, RouteStop

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('label', 'user', 'line1', 'city', 'postal_code', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('user__username', 'user__email', 'label', 'line1', 'city')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'model', 'capacity_kg', 'status')
    list_filter = ('status',)
    search_fields = ('plate_number', 'model')
    ordering = ('plate_number',)
    readonly_fields = ('id',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'license_number', 'active')
    list_filter = ('active',)
    search_fields = ('user__username', 'user__email', 'phone', 'license_number')
    ordering = ('user__username',)
    readonly_fields = ('id',)

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'scheduled_time', 'assigned_driver', 'created_at')
    list_filter = ('status', 'scheduled_time', 'created_at')
    search_fields = ('customer__username', 'customer__email', 'items_description')
    ordering = ('-scheduled_time', '-created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Request Information', {
            'fields': ('customer', 'address', 'scheduled_time', 'items_description', 'estimated_weight_kg')
        }),
        ('Assignment', {
            'fields': ('assigned_driver', 'assigned_vehicle')
        }),
        ('Status', {
            'fields': ('status', 'cancelled_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'driver', 'vehicle', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('name', 'driver__user__username')
    ordering = ('-date', '-created_at')
    readonly_fields = ('id', 'created_at')

@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'pickup', 'sequence', 'eta')
    list_filter = ('route__date', 'eta')
    search_fields = ('route__name', 'pickup__customer__username')
    ordering = ('route', 'sequence')
    readonly_fields = ('id',)
