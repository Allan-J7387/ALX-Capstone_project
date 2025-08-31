from django.contrib import admin
from .models import Route, RouteStop

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_date', 'zone', 'vehicle', 'driver', 'status', 'total_distance_km')
    list_filter = ('status', 'service_date', 'zone', 'created_at')
    search_fields = ('zone__name', 'vehicle__plate_number', 'driver__user__username')
    ordering = ('-service_date', '-created_at')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Route Information', {
            'fields': ('service_date', 'zone', 'total_distance_km')
        }),
        ('Assignment', {
            'fields': ('vehicle', 'driver')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'collection_request', 'sequence', 'status', 'eta', 'arrival_time')
    list_filter = ('status', 'route__service_date', 'eta')
    search_fields = ('route__zone__name', 'collection_request__requester__username')
    ordering = ('route', 'sequence')
    
    fieldsets = (
        ('Stop Information', {
            'fields': ('route', 'collection_request', 'sequence')
        }),
        ('Timing', {
            'fields': ('eta', 'arrival_time', 'departure_time')
        }),
        ('Status', {
            'fields': ('status',)
        })
    )
