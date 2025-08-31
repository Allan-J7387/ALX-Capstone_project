from django.contrib import admin
from .models import Address, Zone

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('label', 'user', 'street', 'city', 'state', 'zipcode', 'created_at')
    list_filter = ('city', 'state', 'created_at')
    search_fields = ('user__username', 'user__email', 'label', 'street', 'city')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
