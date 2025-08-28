import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.collection.models import Address, PickupRequest

User = get_user_model()

@pytest.mark.django_db
def test_create_pickup_request():
    user = User.objects.create_user(username='cust', password='pass123')
    client = APIClient()
    client.force_authenticate(user=user)
    payload = {
        "address": {"label":"Home","line1":"1 Test Ave","city":"City"},
        "scheduled_time": "2025-09-01T09:00:00Z",
        "items_description": "test",
    }
    resp = client.post('/api/v1/pickups/', payload, format='json')
    assert resp.status_code == 201
    assert PickupRequest.objects.filter(customer=user).exists()
