from . import views
from django.urls import path

urlpatterns = [
    path("register/", views.RegistertionAPIView.as_view(), name="api-register")
]
