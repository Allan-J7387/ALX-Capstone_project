from rest_framework import serializers
from .models import Vehicle, Driver


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'plate_number', 'capacity_kg', 'status', 'current_zone']
        read_only_fields = ['id']


class DriverSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    assigned_vehicle_plate = serializers.CharField(source='assigned_vehicle.plate_number', read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'user', 'user_name', 'user_email', 'license_number', 'assigned_vehicle', 'assigned_vehicle_plate']
        read_only_fields = ['id']
