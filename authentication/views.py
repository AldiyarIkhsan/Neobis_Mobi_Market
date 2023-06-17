from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from authentication.serializers import RegistrationSerializer
from rest_framework import serializers


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer

    @swagger_auto_schema(tags=['authentication'], request_body=serializers.RegistrationSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)