from django.contrib import admin
from .models import WasteType, CollectionRequest, RecurrenceSchedule, IssueReport

@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(CollectionRequest)
class CollectionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'waste_type', 'status', 'preferred_date', 'created_at')
    list_filter = ('status', 'waste_type', 'created_at', 'preferred_date')
    search_fields = ('requester__username', 'requester__email', 'notes')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Request Information', {
            'fields': ('requester', 'address', 'waste_type', 'quantity_kg')
        }),
        ('Schedule', {
            'fields': ('preferred_date', 'time_window_start', 'time_window_end')
        }),
        ('Status & Details', {
            'fields': ('status', 'notes', 'photo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RecurrenceSchedule)
class RecurrenceScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'waste_type', 'day_of_week', 'active')
    list_filter = ('day_of_week', 'active', 'waste_type')
    search_fields = ('user__username', 'user__email')
    ordering = ('user', 'day_of_week')

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'status', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Issue Information', {
            'fields': ('user', 'address', 'type', 'description')
        }),
        ('Status & Media', {
            'fields': ('status', 'photo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
