from django.conf import settings
import jwt
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from accounts.models import Profile

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

@pytest.mark.django_db
def test_token_obtain_sucess():
    user = User.objects.create_user(email="test@example.com", password="testpass123", is_verified=True)
    client = APIClient()
    url = reverse("accounts:api-v1:jwt-create") 
    data = {"email": "test@example.com", "password": "testpass123"} 
    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['email'] == user.email
    assert response.data['user_id'] == user.id
 
    
@pytest.mark.django_db
def test_token_obtain_unverified_user():
    user = User.objects.create_user(email="unverified@example.com", password="testpass123", is_verified=False)
    
    client = APIClient()
    url = reverse("accounts:api-v1:jwt-create")
    data = {"email": "unverified@example.com", "password": "testpass123"}
    
    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'details' in response.data
    assert response.data['details'] == ['user is not verified']

@pytest.mark.django_db
def test_token_obtain_wrong_password():
    User.objects.create_user(email="test@example.com", password="correctpass", is_verified=True)
    
    client = APIClient()
    url = reverse("accounts:api-v1:jwt-create")
    data = {"email": "test@example.com", "password": "wrongpass"}
    
    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data 
    assert response.data['detail'] == 'No active account found with the given credentials'
    
@pytest.mark.django_db
def test_token_obtain_missing_fields():
    client = APIClient()
    url = reverse("accounts:api-v1:jwt-create")
    data = {} 
    
    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    assert "password" in response.data


@pytest.mark.django_db
def test_profile_retrieve_and_update():
    user = User.objects.create_user(email="user@example.com", password="testpass", is_verified=True)
    
    Profile.objects.filter(user=user).delete()
    
    profile = Profile.objects.create(
        user=user,
        first_name="Parsa",
        last_name="Javidi",
        bio="Junior developer"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("accounts:api-v1:user-profile")

    # GET profile
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Parsa"
    assert response.data["last_name"] == "Javidi"
    assert response.data["bio"] == "Junior developer"

    # PUT - Update profile
    update_data = {
        "first_name": "Reza",
        "last_name": "Ahmadi",
        "bio": "Senior Developer"
    }

    response = client.put(url, update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Reza"
    assert response.data["last_name"] == "Ahmadi"
    assert response.data["bio"] == "Senior Developer"

    profile.refresh_from_db()
    assert profile.first_name == "Reza"
    assert profile.last_name == "Ahmadi"
    assert profile.bio == "Senior Developer"

@pytest.mark.django_db
def test_password_change_success():
    user = User.objects.create_user(email="test@example.com", password="oldpassword", is_verified=True)
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("accounts:api-v1:change-password")
    data = {
        "old_password": "oldpassword",
        "new_password": "newsecurepassword123",
        "confirm_password": "newsecurepassword123",
    }

    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data["details"] == "Password changed successfully."

    user.refresh_from_db()
    assert user.check_password("newsecurepassword123")

@pytest.mark.django_db
def test_password_change_wrong_old_password():
    user = User.objects.create_user(email="test@example.com", password="oldpassword", is_verified=True)
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("accounts:api-v1:change-password")
    data = {
        "old_password": "wrongoldpass",
        "new_password": "newsecurepassword123",
        "confirm_password": "newsecurepassword123"
    }

    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "old_password" in response.data
    assert response.data["old_password"] == ["Incorrect old password."]

@pytest.mark.django_db
def test_password_change_validation_error():
    user = User.objects.create_user(email="test@example.com", password="oldpassword", is_verified=True)
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("accounts:api-v1:change-password")
    data = {
        "old_password": "", 
        "new_password": "",
        
    }

    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "old_password" in response.data
    assert "new_password" in response.data

@pytest.mark.django_db
def test_password_reset_request_success():
    user = User.objects.create_user(email="user@example.com", password="testpass", is_verified=True)

    client = APIClient()
    url = reverse("accounts:api-v1:password-reset-request")
    response = client.post(url, {"email": "user@example.com"})

    assert response.status_code == 200
    assert response.data["detail"] == "Password reset email has been sent."


@pytest.mark.django_db
def test_password_reset_request_invalid_email():
    client = APIClient()
    url = reverse("accounts:api-v1:password-reset-request")
    response = client.post(url, {"email": "notfound@example.com"})

    assert response.status_code == 400
    assert "email" in response.data
    assert response.data["email"][0] == "No user is associated with this email address."

@pytest.mark.django_db
def test_password_reset_confirm_success():
    user = User.objects.create_user(email="user@example.com", password="oldpass", is_verified=True)

    payload = {"user_id": user.id}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    url = reverse("accounts:api-v1:password-reset-confirm", kwargs={"token": token})
    data = {
        "new_password": "NewStrongPass123!",
        "confirm_password": "NewStrongPass123!",
    }

    client = APIClient()
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    assert response.data["detail"] == "Password has been reset successfully."
    user.refresh_from_db()
    assert user.check_password("NewStrongPass123!") is True


@pytest.mark.django_db
def test_password_reset_confirm_mismatched_passwords():
    user = User.objects.create_user(email="user@example.com", password="oldpass", is_verified=True)
    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")

    url = reverse("accounts:api-v1:password-reset-confirm", kwargs={"token": token})
    data = {
        "new_password": "Password123!",
        "confirm_password": "Mismatch123!",
    }

    client = APIClient()
    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert "detail" in response.data
    assert response.data["detail"][0] == "password doesn't match"


@pytest.mark.django_db
def test_password_reset_confirm_invalid_token():
    url = reverse("accounts:api-v1:password-reset-confirm", kwargs={"token": "invalidtoken"})
    data = {
        "new_password": "AnyPassword123!",
        "confirm_password": "AnyPassword123!",
    }

    client = APIClient()
    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert response.data["detail"] == "Invalid or expired token."