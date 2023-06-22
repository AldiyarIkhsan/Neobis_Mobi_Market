from django.urls import path
from .views import UserRegistrationView, LoginView, SendCodeView, LogoutAPIView, ProfileView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('send-sms/', SendCodeView.as_view(), name='send_sms')
]