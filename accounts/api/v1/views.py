from django.shortcuts import get_object_or_404
from django.urls import reverse
from accounts.models import  Profile
from ..utils import EmailThread
from .serilaizers import (ActivationResendSerializer, 
                          ProfileSerializer, 
                          RegistertionSerializer , 
                          PasswordChangeSerializer , 
                          CustomTokenObtainPairSerializer, 
                          PasswordResetRequestSerializer,
                          PasswordResetConfirmSerializer)

from mail_templated import EmailMessage
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
import jwt
from jwt.exceptions import ExpiredSignatureError , InvalidSignatureError
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class RegisterationAPIView(generics.CreateAPIView):
    '''API view for registering a new user account.'''
    serializer_class = RegistertionSerializer
    
    def perform_create(self, serializer):
        return serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        
        if user.is_verified:
            return Response({{'detail': 'User is already activated.'}}, status=status.HTTP_400_BAD_REQUEST)
        
        token = self.get_tokens_for_user(user)
        
        relative_url = reverse("accounts:api-v1:activation")
        activation_url = self.request.build_absolute_uri(f"{relative_url}?token={token}")
        
        email_obj = EmailMessage('email/activation_email.tpl',
                                 {'token': token, 'user': user, 'activation_url':activation_url},
                                 'admin@gmail.com',
                                 [user.email]
        )
        if email_obj.subject is None:
            email_obj.subject = "Activate Your Account"
        EmailThread(email_obj).start()
        
        headers = self.get_success_headers(serializer.data)
        return Response({'email': user.email, 'message': 'User created. Activation email sent.'},
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
class ActivationApiView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if not token:
            return Response({'detail': 'Token parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except ExpiredSignatureError:
            return Response({'detail':'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidSignatureError:
            return Response({'detail':'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({'detail':'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_obj = get_object_or_404(User, pk=user_id)
        
        if user_obj.is_verified:
            return Response({'detail':'Your account has already been verified'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_obj.is_verified = True
        user_obj.save()
        return Response({'detail':'Your account has been verified successfully'}, status=status.HTTP_200_OK)


from django.conf import settings

class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.get_user()

        # Generate JWT token
        token = self.get_tokens_for_user(user_obj)

        # Build full activation URL
        base_url = getattr(settings, "BASE_URL", "http://127.0.0.1:8000")
        activation_url = f"{base_url}/accounts/api/v1/activation/confirm/?token={token}"

        # Prepare and send email with activation URL and user context
        email_obj = EmailMessage(
            'email/activation_email.tpl',
            {'activation_url': activation_url, 'user': user_obj},
            'admin@gmail.com',
            to=[user_obj.email]
        )
        EmailThread(email_obj).start()

        return Response(
            {'detail': 'Activation email resent successfully.'},
            status=status.HTTP_200_OK
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomTokenObtainPairView(TokenObtainPairView):
    '''Custom JWT token view for handling user authentication'''
    serializer_class = CustomTokenObtainPairSerializer

class ProfileApiView(generics.RetrieveUpdateAPIView):
    '''API view to retrieve and update the authenticated user's profile.'''
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile

class PasswordChangeApiView(generics.GenericAPIView):
    ''' API view to allow authenticated users to change their password.'''
    model = User
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        obj = self.request.user
        return obj 
     
    def put(self , requset):
        serializer = self.get_serializer(data = requset.data)
        
        if serializer.is_valid():
            user = self.get_object()
            
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Incorrect old password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()
            
            return Response({"details":"Password changed successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class PasswordResetRequestApiView(generics.GenericAPIView):
    '''API view to request a password reset via email.'''
    serializer_class = PasswordResetRequestSerializer
    
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        
        user = User.objects.get(email=serializer.validated_data['email'])
        token = self.get_tokens_for_user(user)
        
        relative_url = reverse("accounts:api-v1:password-reset-confirm", kwargs={"token": token})
        reset_url = self.request.build_absolute_uri(relative_url)
        
        email = EmailMessage(
            'email/password_reset_email.tpl',
            {'user': user, 'reset_url': reset_url},
            'admin@gmail.com',
            to=[user.email]
        )
        email.subject = "Password Reset Request"
        EmailThread(email).start()
        
        return Response({'detail': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class PasswordResetConfirmView(generics.GenericAPIView):
    '''API view to confirm password reset using a token.'''
    serializer_class = PasswordResetConfirmSerializer
    
    def post(self, request, token,*args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError , jwt.DecodeError, User.DoesNotExist):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)