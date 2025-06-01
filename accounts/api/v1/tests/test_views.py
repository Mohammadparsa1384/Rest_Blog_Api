from django.conf import settings
import jwt
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
def test_registration_api_view():
    client = APIClient()
    url = reverse("accounts:api-v1:api-register")
    
    data = {
        "email": "testuser@example.com",
        "password": "strongpassword123",
        "password2": "strongpassword123"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'email' in response.data
    assert response.data['email'] == data['email']
    assert 'message' in response.data
    assert response.data['message'] == "User created. Activation email sent."
    
    user_exists = User.objects.filter(email=data['email']).exists()
    assert user_exists

@pytest.mark.django_db
def test_activation_success():
    user = User.objects.create_user(email="test@example.com", password="testpass")
    user.is_verified = False
    user.save()

    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")
    client = APIClient()
    url = reverse("accounts:api-v1:activation", kwargs={"token": token})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Your account has been successfully verified."

    user.refresh_from_db()
    assert user.is_verified is True

@pytest.mark.django_db
def test_activation_expired_token(monkeypatch):
    user = User.objects.create_user(email="test@example.com", password="testpass")
    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")

    def raise_expired(*args, **kwargs):
        raise jwt.ExpiredSignatureError()

    monkeypatch.setattr(jwt, "decode", raise_expired)

    client = APIClient()
    url = reverse("accounts:api-v1:activation", kwargs={"token": token})

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "Activation link has expired."

@pytest.mark.django_db
def test_activation_invalid_signature(monkeypatch):
    user = User.objects.create_user(email="test@example.com", password="testpass")
    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")

    def raise_invalid_signature(*args, **kwargs):
        raise jwt.InvalidSignatureError()

    monkeypatch.setattr(jwt, "decode", raise_invalid_signature)

    client = APIClient()
    url = reverse("accounts:api-v1:activation", kwargs={"token": token})

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_activation_decode_error(monkeypatch):
    user = User.objects.create_user(email="test@example.com", password="testpass")
    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")

    def raise_decode_error(*args, **kwargs):
        raise jwt.DecodeError()

    monkeypatch.setattr(jwt, "decode", raise_decode_error)

    client = APIClient()
    url = reverse("accounts:api-v1:activation", kwargs={"token": token})

    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Token is malformed or invalid."

@pytest.mark.django_db
def test_activation_already_verified():
    user = User.objects.create_user(email="test@example.com", password="testpass")
    user.is_verified = True
    user.save()

    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")
    client = APIClient()
    url = reverse("accounts:api-v1:activation", kwargs={"token": token})

    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Account already verified."