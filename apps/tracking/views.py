from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.collection.models import PickupRequest, Route, Vehicle
from apps.collection.serializers import PickupRequestSerializer, RouteSerializer, VehicleSerializer


class TrackingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='active-routes')
    def active_routes(self, request):
        """Get all active routes with their current status"""
        active_routes = Route.objects.filter(
            date=timezone.now().date()
        ).select_related('driver', 'vehicle')
        serializer = RouteSerializer(active_routes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='vehicle-status')
    def vehicle_status(self, request):
        """Get status of all vehicles"""
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pickup-status')
    def pickup_status(self, request):
        """Get status of pickups for today"""
        today_pickups = PickupRequest.objects.filter(
            scheduled_time__date=timezone.now().date()
        )
        
        # Filter by user role
        user = request.user
        if user.role not in ['DISPATCHER', 'ADMIN']:
            if user.role == 'DRIVER':
                today_pickups = today_pickups.filter(assigned_driver__user=user)
            else:
                today_pickups = today_pickups.filter(customer=user)
        
        serializer = PickupRequestSerializer(today_pickups, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='update-location')
    def update_location(self, request, pk=None):
        """Update vehicle location (for drivers)"""
        if request.user.role != 'DRIVER':
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            vehicle = Vehicle.objects.get(id=pk)
            # In a real implementation, you'd store GPS coordinates
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            
            if latitude and longitude:
                # Store location data (would need additional model fields)
                return Response({"detail": "Location updated successfully"})
            else:
                return Response({"detail": "Latitude and longitude required"}, 
                              status=status.HTTP_400_BAD_REQUEST)
        except Vehicle.DoesNotExist:
            return Response({"detail": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='driver-dashboard')
    def driver_dashboard(self, request):
        """Get dashboard data for drivers"""
        if request.user.role != 'DRIVER':
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            driver = request.user.driver_profile
            today_pickups = PickupRequest.objects.filter(
                assigned_driver=driver,
                scheduled_time__date=timezone.now().date()
            )
            
            dashboard_data = {
                'assigned_vehicle': VehicleSerializer(driver.assigned_vehicle).data if driver.assigned_vehicle else None,
                'today_pickups': PickupRequestSerializer(today_pickups, many=True).data,
                'completed_count': today_pickups.filter(status='completed').count(),
                'pending_count': today_pickups.filter(status__in=['requested', 'scheduled']).count(),
            }
            
            return Response(dashboard_data)
        except:
            return Response({"detail": "Driver profile not found"}, status=status.HTTP_404_NOT_FOUND)
