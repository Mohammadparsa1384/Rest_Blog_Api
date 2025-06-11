import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

client = APIClient()

@pytest.mark.django_db
def test_register_endpoint():
    url = reverse("accounts:api-v1:api-register")
    data = {
        "email": "user@example.com",
        "password": "StrongPass123!",
        "password2": "StrongPass123!"
    }   
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_jwt_create_verified_user():
    user = User.objects.create_user(email="user@example.com", password="StrongPass123!", is_verified=True)
    url = reverse("accounts:api-v1:jwt-create")
    data = {
        "email": "user@example.com",
        "password": "StrongPass123!"
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data

@pytest.mark.django_db
def test_jwt_create_unverified_user():
    User.objects.create_user(email="test2@example.com", password="testpass123", is_verified=False)
    url = reverse("accounts:api-v1:jwt-create")
    data = {
        "email": "test2@example.com",
        "password": "testpass123"
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "details" in response.data

def test_jwt_refresh_token():
    url = reverse("accounts:api-v1:jwt-refresh")
    response = client.post(url, {"refresh": "invalidtoken"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_resend_activation():
    user = User.objects.create_user(email="resend@example.com", password="12345678", is_verified=False)
    url = reverse("accounts:api-v1:resend-activation")
    response = client.post(url, {"email": user.email})
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_password_reset_request():
    User.objects.create_user(email="reset@example.com", password="12345678")
    url = reverse("accounts:api-v1:password-reset-request")
    response = client.post(url, {"email": "reset@example.com"})
    assert response.status_code == status.HTTP_200_OK   

@pytest.mark.django_db
def test_password_change_authenticated(client):
    user = User.objects.create_user(email="changepass@example.com", password="oldPass123", is_verified=True)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("accounts:api-v1:change-password")
    data = {
        "old_password": "oldPass123",
        "new_password": "NewPass123!",
        "confirm_password": "NewPass123!"
    }
    response = client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_profile_get_authenticated():
    user = User.objects.create_user(email="profile@example.com", password="12345678", is_verified=True)
    client.force_authenticate(user=user)
    url = reverse("accounts:api-v1:user-profile")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK