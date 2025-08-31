from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at', 'due_date', 'paid_date')
    list_filter = ('status', 'created_at', 'due_date', 'paid_date')
    search_fields = ('customer__username', 'customer__email', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'paid_date')
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('customer', 'total_amount', 'description')
        }),
        ('Status & Dates', {
            'fields': ('status', 'due_date', 'paid_date')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_paid', 'mark_as_overdue']
    
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='PAID', paid_date=timezone.now())
    mark_as_paid.short_description = "Mark selected invoices as paid"
    
    def mark_as_overdue(self, request, queryset):
        queryset.update(status='OVERDUE')
    mark_as_overdue.short_description = "Mark selected invoices as overdue"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date', 'created_at')
    search_fields = ('invoice__customer__username', 'payment_reference')
    ordering = ('-payment_date',)
    readonly_fields = ('id', 'payment_date', 'created_at')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('invoice', 'amount', 'payment_method', 'payment_reference')
        }),
        ('Timestamps', {
            'fields': ('payment_date', 'created_at'),
            'classes': ('collapse',)
        })
    )
