from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    collection_requests = serializers.DictField()
    pickup_requests = serializers.DictField()
    vehicles = serializers.DictField()
    users = serializers.DictField()


class CollectionStatsSerializer(serializers.Serializer):
    status_distribution = serializers.ListField()
    weekly_trend = serializers.ListField()


class VehicleUtilizationSerializer(serializers.Serializer):
    vehicle_id = serializers.CharField()
    plate_number = serializers.CharField()
    status = serializers.CharField()
    today_pickups = serializers.IntegerField()
    capacity_kg = serializers.IntegerField()


class UserStatsSerializer(serializers.Serializer):
    role_distribution = serializers.ListField()
    active_users_last_30_days = serializers.IntegerField()
    total_users = serializers.IntegerField()
