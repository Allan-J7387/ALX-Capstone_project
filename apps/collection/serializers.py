from rest_framework import serializers
from .models import CollectionRequest
from .models import PickupRequest, Address, Driver, Vehicle

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'user')

class PickupRequestSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.id')
    address = AddressSerializer()

    class Meta:
        model = PickupRequest
        fields = ['id','customer','address','scheduled_time','items_description','estimated_weight_kg','status','assigned_driver','assigned_vehicle','created_at']

    def create(self, validated_data):
        # nested address handling
        address_data = validated_data.pop('address')
        user = self.context['request'].user
        address, _ = Address.objects.get_or_create(user=user, line1=address_data.get('line1'), city=address_data.get('city'), defaults=address_data)
        validated_data['address'] = address
        validated_data['customer'] = user
        return super().create(validated_data)

class CollectionRequestSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        model = CollectionRequest
        fields = "__all__"