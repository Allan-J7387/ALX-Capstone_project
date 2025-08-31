from rest_framework import serializers
from .models import CollectionRequest, WasteType, IssueReport, RecurrenceSchedule
from apps.locations.serializers import AddressSerializer
from apps.locations.models import Address

class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteType
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class CollectionRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source="requester.username", read_only=True)
    address_details = AddressSerializer(source="address", read_only=True)
    waste_type_name = serializers.CharField(source="waste_type.name", read_only=True)

    class Meta:
        model = CollectionRequest
        fields = ['id', 'requester', 'requester_name', 'address', 'address_details', 
                 'waste_type', 'waste_type_name', 'quantity_kg', 'preferred_date', 
                 'time_window_start', 'time_window_end', 'status', 'photo', 
                 'created_at', 'updated_at', 'notes']
        read_only_fields = ['id', 'requester', 'created_at', 'updated_at']

class RecurrenceScheduleSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    address_details = AddressSerializer(source="address", read_only=True)
    waste_type_name = serializers.CharField(source="waste_type.name", read_only=True)

    class Meta:
        model = RecurrenceSchedule
        fields = ['id', 'user', 'user_name', 'address', 'address_details', 
                 'waste_type', 'waste_type_name', 'day_of_week', 
                 'time_window_start', 'time_window_end', 'active']
        read_only_fields = ['id', 'user']

class IssueReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    address_details = AddressSerializer(source="address", read_only=True)

    class Meta:
        model = IssueReport
        fields = ['id', 'user', 'user_name', 'address', 'address_details', 
                 'type', 'description', 'photo', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
