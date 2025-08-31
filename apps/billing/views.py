from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from decimal import Decimal
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
from apps.collection.models import PickupRequest


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['DISPATCHER', 'ADMIN']:
            return Invoice.objects.all()
        return Invoice.objects.filter(customer=user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='mark-paid')
    def mark_paid(self, request, pk=None):
        if request.user.role not in ['DISPATCHER', 'ADMIN']:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        invoice = self.get_object()
        payment_method = request.data.get('payment_method', 'CASH')
        
        # Create payment record
        Payment.objects.create(
            invoice=invoice,
            amount=invoice.total_amount,
            payment_method=payment_method,
            payment_date=timezone.now()
        )
        
        invoice.status = 'PAID'
        invoice.paid_date = timezone.now()
        invoice.save()
        
        return Response({"detail": "Invoice marked as paid"})

    @action(detail=False, methods=['post'], url_path='generate-from-pickups')
    def generate_from_pickups(self, request):
        if request.user.role not in ['DISPATCHER', 'ADMIN']:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        customer_id = request.data.get('customer_id')
        pickup_ids = request.data.get('pickup_ids', [])
        
        if not customer_id or not pickup_ids:
            return Response({"detail": "customer_id and pickup_ids required"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate total from completed pickups
        pickups = PickupRequest.objects.filter(
            id__in=pickup_ids,
            customer_id=customer_id,
            status='completed'
        )
        
        if not pickups.exists():
            return Response({"detail": "No completed pickups found"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Simple pricing: $10 per pickup + $5 per estimated kg
        total_amount = Decimal('0.00')
        for pickup in pickups:
            base_cost = Decimal('10.00')  # Base pickup cost
            weight_cost = Decimal('5.00') * Decimal(str(pickup.estimated_weight_kg or 0))
            total_amount += base_cost + weight_cost
        
        invoice = Invoice.objects.create(
            customer_id=customer_id,
            total_amount=total_amount,
            due_date=timezone.now().date() + timezone.timedelta(days=30),
            description=f"Waste collection services for {pickups.count()} pickups"
        )
        
        return Response(self.get_serializer(invoice).data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['DISPATCHER', 'ADMIN']:
            return Payment.objects.all()
        return Payment.objects.filter(invoice__customer=user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
