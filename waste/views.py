from rest_framework import viewsets, permissions
from .models import CollectionRequest, WasteType
from .serializers import CollectionRequestSerializer, WasteTypeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class IsCitizen(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "CITIZEN"

class CollectionRequestViewSet(viewsets.ModelViewSet):
    queryset = CollectionRequest.objects.all().select_related("requester", "address", "waste_type")
    serializer_class = CollectionRequestSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated(), IsCitizen()]
        if self.action in ["partial_update", "update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role in ("DISPATCHER", "ADMIN"):
            qs = self.queryset
        else:
            qs = self.queryset.filter(requester=user)
        # add filtering by status/date params
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    @action(detail=True, methods=["post"], url_path="schedule", permission_classes=[permissions.IsAuthenticated])
    def schedule(self, request, pk=None):
        # dispatcher assigns this request to a route (implementation stub)
        return Response({"detail": "scheduling stub"})
