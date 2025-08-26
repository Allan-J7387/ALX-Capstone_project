from rest_framework import serializers
from .models import CollectionRequest, WasteType, IssueReport
from apps.locations.serializers import AddressSerializer

class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteType
        fields = "__all__"

class CollectionRequestSerializer(serializers.ModelSerializer):
    requester = serializers.ReadOnlyField(source="requester.id")
    address = serializers.PrimaryKeyRelatedField(queryset=None)  # set in view init

    class Meta:
        model = CollectionRequest
        read_only_fields = ("status", "created_at", "updated_at")
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["requester"] = request.user
        return super().create(validated_data)
