import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from ..serilaizers import (PasswordResetConfirmSerializer, 
                           RegistertionSerializer,
                           CustomTokenObtainPairSerializer,
                           ActivationResendSerializer,
                           PasswordResetRequestSerializer,
                           )


User = get_user_model()


@pytest.mark.django_db
def test_registration_serializer_valid():
    data = {
        "email": "test@example.com",
        "password": "StrongPass123!",
        "password2": "StrongPass123!"
    }
    serializer = RegistertionSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.check_password(data["password"])

@pytest.mark.django_db
def test_registration_serializer_password_mismatch():
    data = {
        "email": "test@example.com",
        "password": "StrongPass123!",
        "password2": "WrongPass123!"
    }
    serializer = RegistertionSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors

@pytest.mark.django_db
def test_token_obtain_pair_verified_user():
    user = User.objects.create_user(email="verified@example.com", password="StrongPass123!", is_verified=True)
    data = {
        "email": "verified@example.com",
        "password": "StrongPass123!"
    }
    
    serializer = CustomTokenObtainPairSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert "access" in serializer.validated_data

@pytest.mark.django_db
def test_token_obtain_pair_unverified_user():
    user = User.objects.create_user(email="unverified@example.com", password="StrongPass123!", is_verified=False)
    data = {
        "email": "unverified@example.com",
        "password": "StrongPass123!"
    }
    serializer = CustomTokenObtainPairSerializer(data=data)
    assert not serializer.is_valid()
    assert "details" in serializer.errors

@pytest.mark.django_db
def test_activation_resend_valid():
    user = User.objects.create_user(email="test@example.com", password="12345678", is_verified=False)
    serializer = ActivationResendSerializer(data={"email": user.email})
    assert serializer.is_valid(), serializer.errors
    assert serializer.get_user() == user

@pytest.mark.django_db
def test_activation_resend_user_not_found():
    serializer = ActivationResendSerializer(data={"email": "notfound@example.com"})
    assert not serializer.is_valid()
    assert "detail" in serializer.errors

@pytest.mark.django_db
def test_password_reset_request_valid():
    User.objects.create_user(email="reset@example.com", password="12345678")
    serializer = PasswordResetRequestSerializer(data={"email": "reset@example.com"})
    assert serializer.is_valid()

@pytest.mark.django_db
def test_password_reset_request_invalid():
    serializer = PasswordResetRequestSerializer(data={"email": "wrong@example.com"})
    assert not serializer.is_valid()

def test_password_reset_confirm_valid():
    data = {
        "new_password": "NewPassword123!",
        "confirm_password": "NewPassword123!"
    }
    serializer = PasswordResetConfirmSerializer(data=data)
    assert serializer.is_valid()

def test_password_reset_confirm_mismatch():
    data = {
        "new_password": "NewPassword123!",
        "confirm_password": "WrongPassword!"
    }
    serializer = PasswordResetConfirmSerializer(data=data)
    assert not serializer.is_valid()
    assert "detail" in serializer.errors