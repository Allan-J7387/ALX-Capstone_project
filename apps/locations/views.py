from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Address, Zone
from .serializers import AddressSerializer, ZoneSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ['DISPATCHER', 'ADMIN']:
            return Address.objects.all()
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='by-zone')
    def addresses_by_zone(self, request):
        zone_id = request.query_params.get('zone_id')
        if zone_id:
            # This would require implementing zone-address relationships
            addresses = self.get_queryset()
            serializer = self.get_serializer(addresses, many=True)
            return Response(serializer.data)
        return Response({'detail': 'zone_id parameter required'}, 
                       status=status.HTTP_400_BAD_REQUEST)


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['get'], url_path='addresses')
    def zone_addresses(self, request, pk=None):
        zone = self.get_object()
        # This would require implementing zone-address relationships
        addresses = Address.objects.all()  # Placeholder
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
