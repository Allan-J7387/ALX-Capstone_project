from rest_framework import viewsets, permissions, status
from .models import CollectionRequest, WasteType, RecurrenceSchedule, IssueReport
from .serializers import CollectionRequestSerializer, WasteTypeSerializer, RecurrenceScheduleSerializer, IssueReportSerializer
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
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    @action(detail=True, methods=["post"], url_path="schedule", permission_classes=[permissions.IsAuthenticated])
    def schedule(self, request, pk=None):
        collection_request = self.get_object()
        if request.user.role not in ["DISPATCHER", "ADMIN"]:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        scheduled_date = request.data.get('scheduled_date')
        if scheduled_date:
            collection_request.status = "SCHEDULED"
            collection_request.save()
            return Response({"detail": "Request scheduled successfully"})
        return Response({"detail": "scheduled_date required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        collection_request = self.get_object()
        if request.user.role not in ["DRIVER", "DISPATCHER", "ADMIN"]:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        collection_request.status = "COMPLETED"
        collection_request.save()
        return Response({"detail": "Request completed successfully"})

class WasteTypeViewSet(viewsets.ModelViewSet):
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class RecurrenceScheduleViewSet(viewsets.ModelViewSet):
    queryset = RecurrenceSchedule.objects.all()
    serializer_class = RecurrenceScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ("DISPATCHER", "ADMIN"):
            return RecurrenceSchedule.objects.all()
        return RecurrenceSchedule.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IssueReportViewSet(viewsets.ModelViewSet):
    queryset = IssueReport.objects.all()
    serializer_class = IssueReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ("DISPATCHER", "ADMIN"):
            return IssueReport.objects.all()
        return IssueReport.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="acknowledge")
    def acknowledge(self, request, pk=None):
        issue = self.get_object()
        if request.user.role not in ["DISPATCHER", "ADMIN"]:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        issue.status = "ACKNOWLEDGED"
        issue.save()
        return Response({"detail": "Issue acknowledged"})

    @action(detail=True, methods=["post"], url_path="resolve")
    def resolve(self, request, pk=None):
        issue = self.get_object()
        if request.user.role not in ["DISPATCHER", "ADMIN"]:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        issue.status = "RESOLVED"
        issue.save()
        return Response({"detail": "Issue resolved"})
