from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
from apps.waste.models import CollectionRequest
from apps.collection.models import PickupRequest, Vehicle
from apps.accounts.models import User


class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['dashboard', 'collection_stats', 'vehicle_utilization', 'user_stats']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        """Get dashboard analytics data"""
        if request.user.role not in ['DISPATCHER', 'ADMIN']:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Collection requests stats
        total_requests = CollectionRequest.objects.count()
        pending_requests = CollectionRequest.objects.filter(status='PENDING').count()
        completed_today = CollectionRequest.objects.filter(
            status='COMPLETED',
            updated_at__date=today
        ).count()
        
        # Pickup requests stats
        total_pickups = PickupRequest.objects.count()
        scheduled_today = PickupRequest.objects.filter(
            scheduled_time__date=today
        ).count()
        
        # Vehicle stats
        active_vehicles = Vehicle.objects.filter(status='active').count()
        total_vehicles = Vehicle.objects.count()
        
        # User stats
        total_users = User.objects.count()
        active_drivers = User.objects.filter(role='DRIVER', is_active=True).count()
        
        dashboard_data = {
            'collection_requests': {
                'total': total_requests,
                'pending': pending_requests,
                'completed_today': completed_today,
            },
            'pickup_requests': {
                'total': total_pickups,
                'scheduled_today': scheduled_today,
            },
            'vehicles': {
                'active': active_vehicles,
                'total': total_vehicles,
                'utilization_rate': (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
            },
            'users': {
                'total': total_users,
                'active_drivers': active_drivers,
            }
        }
        
        return Response(dashboard_data)

    @action(detail=False, methods=['get'], url_path='collection-stats')
    def collection_stats(self, request):
        """Get collection statistics"""
        if request.user.role not in ['DISPATCHER', 'ADMIN']:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        # Status distribution
        status_stats = CollectionRequest.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Weekly trend
        week_ago = timezone.now().date() - timedelta(days=7)
        weekly_stats = []
        for i in range(7):
            date = week_ago + timedelta(days=i)
            count = CollectionRequest.objects.filter(
                created_at__date=date
            ).count()
            weekly_stats.append({
                'date': date.isoformat(),
                'count': count
            })
        
        return Response({
            'status_distribution': list(status_stats),
            'weekly_trend': weekly_stats
        })

    @action(detail=False, methods=['get'], url_path='vehicle-utilization')
    def vehicle_utilization(self, request):
        """Get vehicle utilization statistics"""
        if request.user.role not in ['DISPATCHER', 'ADMIN']:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        vehicles = Vehicle.objects.all()
        utilization_data = []
        
        for vehicle in vehicles:
            today_pickups = PickupRequest.objects.filter(
                assigned_vehicle=vehicle,
                scheduled_time__date=timezone.now().date()
            ).count()
            
            utilization_data.append({
                'vehicle_id': str(vehicle.id),
                'plate_number': vehicle.plate_number,
                'status': vehicle.status,
                'today_pickups': today_pickups,
                'capacity_kg': vehicle.capacity_kg
            })
        
        return Response(utilization_data)

    @action(detail=False, methods=['get'], url_path='user-stats')
    def user_stats(self, request):
        """Get user statistics"""
        if request.user.role not in ['DISPATCHER', 'ADMIN']:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        # User role distribution
        role_stats = User.objects.values('role').annotate(
            count=Count('id')
        )
        
        # Active users in last 30 days
        month_ago = timezone.now() - timedelta(days=30)
        active_users = User.objects.filter(
            last_login__gte=month_ago
        ).count()
        
        return Response({
            'role_distribution': list(role_stats),
            'active_users_last_30_days': active_users,
            'total_users': User.objects.count()
        })
