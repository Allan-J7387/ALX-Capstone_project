from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PickupRequestViewSet, AddressViewSet, VehicleViewSet, DriverViewSet, RouteViewSet, RouteStopViewSet

router = DefaultRouter()
router.register(r'pickup-requests', PickupRequestViewSet, basename='pickuprequest')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'route-stops', RouteStopViewSet, basename='routestop')

urlpatterns = [
    path('', include(router.urls)),
]
