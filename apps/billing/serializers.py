from rest_framework import serializers
from .models import Invoice, Payment


class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    payments_total = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'customer_name', 'customer_email', 'total_amount', 
                 'description', 'status', 'created_at', 'due_date', 'paid_date', 
                 'payments_total', 'is_overdue']
        read_only_fields = ['id', 'created_at', 'paid_date']

    def get_payments_total(self, obj):
        return sum(payment.amount for payment in obj.payments.all())

    def get_is_overdue(self, obj):
        from django.utils import timezone
        if obj.due_date and obj.status == 'PENDING':
            return timezone.now().date() > obj.due_date
        return False


class PaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.id', read_only=True)
    customer_name = serializers.CharField(source='invoice.customer.username', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'invoice_number', 'customer_name', 'amount', 
                 'payment_method', 'payment_reference', 'payment_date', 'created_at']
        read_only_fields = ['id', 'payment_date', 'created_at']
