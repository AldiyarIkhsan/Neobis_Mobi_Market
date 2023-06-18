from django.urls import path
from .views import UserRegistrationView, LoginAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginAPIView.as_view(), name="login")
]