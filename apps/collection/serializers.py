from rest_framework import serializers
from .models import PickupRequest, Address, Driver, Vehicle, Route, RouteStop

class AddressSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'user', 'user_name', 'label', 'line1', 'line2', 'city', 'postal_code', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'plate_number', 'model', 'capacity_kg', 'status']
        read_only_fields = ['id']

class DriverSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'user', 'user_name', 'user_email', 'phone', 'license_number', 'active']
        read_only_fields = ['id']

class PickupRequestSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    address_details = AddressSerializer(source='address', read_only=True)
    driver_name = serializers.CharField(source='assigned_driver.user.username', read_only=True)
    vehicle_plate = serializers.CharField(source='assigned_vehicle.plate_number', read_only=True)

    class Meta:
        model = PickupRequest
        fields = ['id', 'customer', 'customer_name', 'address', 'address_details', 
                 'scheduled_time', 'items_description', 'estimated_weight_kg', 'status', 
                 'assigned_driver', 'driver_name', 'assigned_vehicle', 'vehicle_plate', 
                 'created_at', 'updated_at', 'cancelled_reason']
        read_only_fields = ['id', 'customer', 'created_at', 'updated_at']

class RouteSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.user.username', read_only=True)
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)
    stops_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'name', 'date', 'driver', 'driver_name', 'vehicle', 'vehicle_plate', 
                 'stops_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_stops_count(self, obj):
        return obj.stops.count()

class RouteStopSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.name', read_only=True)
    pickup_details = PickupRequestSerializer(source='pickup', read_only=True)

    class Meta:
        model = RouteStop
        fields = ['id', 'route', 'route_name', 'pickup', 'pickup_details', 'sequence', 'eta']
        read_only_fields = ['id']