from .serilaizers import RegistertionSerializer
from rest_framework import generics

class RegistertionAPIView(generics.CreateAPIView):
    '''API view for registering a new user account.'''
    serializer_class = RegistertionSerializer
