from django.contrib import admin
from .models import GPSLog

@admin.register(GPSLog)
class GPSLogAdmin(admin.ModelAdmin):
    list_display = ('route', 'timestamp', 'latitude', 'longitude', 'speed')
    list_filter = ('timestamp', 'route__service_date')
    search_fields = ('route__zone__name', 'route__vehicle__plate_number')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
