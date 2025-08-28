from rest_framework.routers import DefaultRouter
from .views import PickupRequestViewSet

router = DefaultRouter()
router.register(r'pickups', PickupRequestViewSet, basename='pickup')

urlpatterns = router.urls
