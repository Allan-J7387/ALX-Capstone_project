from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CollectionRequest, Address
from .serializers import CollectionRequestSerializer, AddressSerializer


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class CollectionRequestViewSet(viewsets.ModelViewSet):
    queryset = CollectionRequest.objects.all()
    serializer_class = CollectionRequestSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CollectionRequest.objects.all()
        return CollectionRequest.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        pickup = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(CollectionRequest.STATUS_CHOICES):
            return Response({'detail':'invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        pickup.status = new_status
        pickup.save()
        return Response(self.get_serializer(pickup).data)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
