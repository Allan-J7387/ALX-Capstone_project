from rest_framework import serializers
from apps.collection.models import PickupRequest, Route, Vehicle
from apps.collection.serializers import PickupRequestSerializer, VehicleSerializer


class TrackingRouteSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.user.username', read_only=True)
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)
    stops_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'name', 'date', 'driver_name', 'vehicle_plate', 'stops_count', 'created_at']

    def get_stops_count(self, obj):
        return obj.stops.count()


class TrackingPickupSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    address_details = serializers.CharField(source='address.line1', read_only=True)
    driver_name = serializers.CharField(source='assigned_driver.user.username', read_only=True)
    vehicle_plate = serializers.CharField(source='assigned_vehicle.plate_number', read_only=True)

    class Meta:
        model = PickupRequest
        fields = ['id', 'customer_name', 'address_details', 'scheduled_time', 'status', 
                 'driver_name', 'vehicle_plate', 'estimated_weight_kg']


class VehicleLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    timestamp = serializers.DateTimeField(read_only=True)
