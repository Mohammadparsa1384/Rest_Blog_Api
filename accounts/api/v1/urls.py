from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api-v1"

urlpatterns = [
    # registration
    path("register/", views.RegisterationAPIView.as_view(), name="api-register"),
    
    # activation
    path("activation/confirm/", views.ActivationApiView.as_view(), name="activation"),
    # resend activation
    path("activation/resend/", views.ActivationResendApiView.as_view(), name="resend-activation"),
    
    # change password
    path("change-password/", views.PasswordChangeApiView.as_view() , name="change-password"),
    
    
    # login jwt
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    # profile endpoint
    path("profile/", views.ProfileApiView.as_view(),name="user-profile"),
    
]
