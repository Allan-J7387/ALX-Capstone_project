from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.collection.models import Route, RouteStop
from apps.collection.serializers import RouteSerializer, RouteStopSerializer
from apps.waste.models import CollectionRequest


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

    @action(detail=True, methods=['post'], url_path='optimize')
    def optimize_route(self, request, pk=None):
        route = self.get_object()
        if request.user.role not in ["DISPATCHER", "ADMIN"]:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        # Placeholder for route optimization logic
        return Response({"detail": "Route optimization completed"})

    @action(detail=False, methods=['post'], url_path='create-from-requests')
    def create_from_requests(self, request):
        if request.user.role not in ["DISPATCHER", "ADMIN"]:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        request_ids = request.data.get('request_ids', [])
        driver_id = request.data.get('driver_id')
        vehicle_id = request.data.get('vehicle_id')
        
        if not request_ids:
            return Response({"detail": "request_ids required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create route and add stops
        route = Route.objects.create(
            name=f"Route {Route.objects.count() + 1}",
            driver_id=driver_id,
            vehicle_id=vehicle_id
        )
        
        for i, request_id in enumerate(request_ids):
            try:
                collection_request = CollectionRequest.objects.get(id=request_id)
                RouteStop.objects.create(
                    route=route,
                    pickup_id=request_id,
                    sequence=i + 1
                )
                collection_request.status = "SCHEDULED"
                collection_request.save()
            except CollectionRequest.DoesNotExist:
                continue
        
        return Response(self.get_serializer(route).data)


class RouteStopViewSet(viewsets.ModelViewSet):
    queryset = RouteStop.objects.all()
    serializer_class = RouteStopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='mark-completed')
    def mark_completed(self, request, pk=None):
        stop = self.get_object()
        if request.user.role not in ["DRIVER", "DISPATCHER", "ADMIN"]:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        if stop.pickup:
            stop.pickup.status = "COMPLETED"
            stop.pickup.save()
        
        return Response({"detail": "Stop marked as completed"})
