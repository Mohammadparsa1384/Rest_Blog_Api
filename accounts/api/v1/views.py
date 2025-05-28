from .serilaizers import RegistertionSerializer
from rest_framework import generics

class RegistertionAPIView(generics.CreateAPIView):
    serializer_class = RegistertionSerializer
