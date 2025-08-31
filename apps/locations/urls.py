from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet, ZoneViewSet

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'zones', ZoneViewSet, basename='zone')

urlpatterns = [
    path('', include(router.urls)),
]
