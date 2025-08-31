from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['DISPATCHER', 'ADMIN']:
            return Notification.objects.all()
        return Notification.objects.filter(user=user)

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({"detail": "Notification marked as read"})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        user_notifications = self.get_queryset().filter(is_read=False)
        user_notifications.update(is_read=True, read_at=timezone.now())
        return Response({"detail": f"Marked {user_notifications.count()} notifications as read"})

    @action(detail=False, methods=['get'], url_path='unread')
    def unread_notifications(self, request):
        unread = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(unread, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({"unread_count": count})

    @action(detail=False, methods=['post'], url_path='send-notification')
    def send_notification(self, request):
        if request.user.role not in ['DISPATCHER', 'ADMIN']:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        message = request.data.get('message')
        notification_type = request.data.get('type', 'INFO')
        
        if not user_id or not message:
            return Response({"detail": "user_id and message required"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        notification = Notification.objects.create(
            user_id=user_id,
            message=message,
            type=notification_type
        )
        
        return Response(self.get_serializer(notification).data)
