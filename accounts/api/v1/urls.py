from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api-v1"

urlpatterns = [
    # registration
    path("register/", views.RegisterationAPIView.as_view(), name="api-register"),
    
    # activation
    path("activation/confirm/<str:token>", views.ActivationApiView.as_view(), name="activation"),
    # resend activation
    path("activation/resend/", views.ActivationResendApiView.as_view(), name="resend-activation"),
    
    # change password
    path("change-password/", views.PasswordChangeApiView.as_view() , name="change-password"),
    
    # password reset
    path("password-reset/",views.PasswordResetRequestApiView.as_view(), name="password-reset-request"),
    path('password/reset/confirm/<str:token>', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    
    
    # login jwt
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    # profile endpoint
    path("profile/", views.ProfileApiView.as_view(),name="user-profile"),
    
]
