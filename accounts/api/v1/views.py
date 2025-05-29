from django.shortcuts import get_object_or_404
from accounts.models import CustomUser, Profile
from ..utils import EmailThread
from .serilaizers import ProfileSerializer, RegistertionSerializer ,CustomTokenObtainPairSerializer
from mail_templated import EmailMessage
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
import jwt
from jwt.exceptions import ExpiredSignatureError , InvalidSignatureError
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

class RegisterationAPIView(generics.CreateAPIView):
    '''API view for registering a new user account.'''
    serializer_class = RegistertionSerializer
    
    def perform_create(self, serializer):
        return serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token = self.get_tokens_for_user(user)
        
        email_obj = EmailMessage('email/activation_email.tpl',
                                 {'token': token, 'user': user},
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
        
        user_obj = get_object_or_404(CustomUser, pk=user_id)
        
        if user_obj.is_verified:
            return Response({'detail':'Your account has already been verified'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_obj.is_verified = True
        user_obj.save()
        return Response({'detail':'Your account has been verified successfully'}, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    '''Custom jwt Token view '''
    serializer_class = CustomTokenObtainPairSerializer

class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile