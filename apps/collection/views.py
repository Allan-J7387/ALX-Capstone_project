from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PickupRequest, Address, Vehicle, Driver, Route, RouteStop
from .serializers import PickupRequestSerializer, AddressSerializer, VehicleSerializer, DriverSerializer, RouteSerializer, RouteStopSerializer


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class PickupRequestViewSet(viewsets.ModelViewSet):
    queryset = PickupRequest.objects.all()
    serializer_class = PickupRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ['DISPATCHER', 'ADMIN']:
            return PickupRequest.objects.all()
        return PickupRequest.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        pickup = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(PickupRequest.STATUS_CHOICES):
            return Response({'detail':'invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        pickup.status = new_status
        pickup.save()
        return Response(self.get_serializer(pickup).data)

    @action(detail=True, methods=['post'], url_path='assign-driver')
    def assign_driver(self, request, pk=None):
        pickup = self.get_object()
        driver_id = request.data.get('driver_id')
        vehicle_id = request.data.get('vehicle_id')
        
        if driver_id:
            try:
                driver = Driver.objects.get(id=driver_id)
                pickup.assigned_driver = driver
            except Driver.DoesNotExist:
                return Response({'detail': 'Driver not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
                pickup.assigned_vehicle = vehicle
            except Vehicle.DoesNotExist:
                return Response({'detail': 'Vehicle not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        pickup.save()
        return Response(self.get_serializer(pickup).data)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ['DISPATCHER', 'ADMIN']:
            return Address.objects.all()
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['get'], url_path='stops')
    def get_stops(self, request, pk=None):
        route = self.get_object()
        stops = route.stops.all().order_by('sequence')
        serializer = RouteStopSerializer(stops, many=True)
        return Response(serializer.data)

class RouteStopViewSet(viewsets.ModelViewSet):
    queryset = RouteStop.objects.all()
    serializer_class = RouteStopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
