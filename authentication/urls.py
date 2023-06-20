from django.urls import path
from .views import UserRegistrationView, LoginAPIView, SendSMSView, LogoutAPIView, ProfileView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('send-sms/', SendSMSView.as_view(), name='send_sms')
]