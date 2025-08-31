from rest_framework import serializers
from apps.collection.models import Route, RouteStop
from apps.collection.serializers import DriverSerializer, VehicleSerializer, PickupRequestSerializer


class RouteSerializer(serializers.ModelSerializer):
    driver_details = DriverSerializer(source='driver', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    stops_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'name', 'date', 'driver', 'driver_details', 'vehicle', 'vehicle_details', 'stops_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_stops_count(self, obj):
        return obj.stops.count()


class RouteStopSerializer(serializers.ModelSerializer):
    pickup_details = PickupRequestSerializer(source='pickup', read_only=True)
    route_name = serializers.CharField(source='route.name', read_only=True)

    class Meta:
        model = RouteStop
        fields = ['id', 'route', 'route_name', 'pickup', 'pickup_details', 'sequence', 'eta']
        read_only_fields = ['id']
