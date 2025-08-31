from rest_framework import serializers
from .models import Address, Zone

class AddressSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'user', 'user_name', 'label', 'street', 'city', 'state', 'zipcode', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name', 'polygon_geojson']
        read_only_fields = ['id']
