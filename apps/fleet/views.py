from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vehicle, Driver
from .serializers import VehicleSerializer, DriverSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        vehicle = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Vehicle.STATUS):
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        vehicle.status = new_status
        vehicle.save()
        return Response(self.get_serializer(vehicle).data)

    @action(detail=False, methods=['get'], url_path='available')
    def available_vehicles(self, request):
        available = self.queryset.filter(status='AVAILABLE')
        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='assign-vehicle')
    def assign_vehicle(self, request, pk=None):
        driver = self.get_object()
        vehicle_id = request.data.get('vehicle_id')
        
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id, status='AVAILABLE')
                driver.assigned_vehicle = vehicle
                driver.save()
                return Response(self.get_serializer(driver).data)
            except Vehicle.DoesNotExist:
                return Response({'detail': 'Vehicle not found or not available'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        else:
            driver.assigned_vehicle = None
            driver.save()
            return Response(self.get_serializer(driver).data)

    @action(detail=False, methods=['get'], url_path='active')
    def active_drivers(self, request):
        active = self.queryset.filter(user__is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)
