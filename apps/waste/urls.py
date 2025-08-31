from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectionRequestViewSet, WasteTypeViewSet, RecurrenceScheduleViewSet, IssueReportViewSet

router = DefaultRouter()
router.register(r'collection-requests', CollectionRequestViewSet, basename='collectionrequest')
router.register(r'waste-types', WasteTypeViewSet, basename='wastetype')
router.register(r'recurrence-schedules', RecurrenceScheduleViewSet, basename='recurrenceschedule')
router.register(r'issue-reports', IssueReportViewSet, basename='issuereport')

urlpatterns = [
    path('', include(router.urls)),
]
