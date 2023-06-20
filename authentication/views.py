from django.contrib.auth import get_user_model
from rest_framework import generics, status, views
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from twilio.rest import Client
from django.conf import settings
from .models import User
from rest_framework import viewsets
from rest_framework import generics, status, views, permissions


class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request: Request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={200: 'User updated successfully', 400: 'Bad Request'}
    )

    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendSMSView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        message = request.data.get('message')

        if phone and message:
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone
                )
                return Response({'status': 'success', 'message': 'SMS sent successfully'})
            except Exception as e:
                return Response({'status':'error', 'message': str(e)})
        else:
            return Response({'status': 'error', 'message': 'phone and message are required.'})