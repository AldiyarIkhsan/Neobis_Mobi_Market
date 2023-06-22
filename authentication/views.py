from django.contrib.auth import get_user_model
from rest_framework import generics, status, views
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer, ProfileSerializer, SendCodeSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from twilio.rest import Client
from django.conf import settings
from .models import User
from rest_framework import viewsets
from rest_framework import generics, status, views, permissions
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics, exceptions, permissions



class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request: Request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 'success',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    @swagger_auto_schema(request_body=ProfileSerializer,
                         responses={200: 'User updated successfully', 400: 'Bad Request'})
    def put(self, request):
        user = request.user

        serializer = ProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendCodeView(APIView):
    serializer_class = SendCodeSerializer

    @swagger_auto_schema(request_body=SendCodeSerializer,
                         responses={200: 'User updated successfully', 400: 'Bad Request'})
    def put(self, request):
        user = request.user

        serializer = SendCodeSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            try:
                user = User.objects.get(phone_number=user_data["phone_number"])
            except User.DoesNotExist:
                raise NotAcceptable("Please enter a valid phone.")

            code = ''.join(random.choice(string.digits) for _ in range(4))
            VerifyPhone.objects.create(phone=user.phone_number, code=code)
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f"Your verification code pin is {code}",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=user.phone_number
                )
                return Response({'status': 'success', 'message': 'SMS sent successfully.'})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            return Response({'message': 'User updated successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneVerifyView(APIView):
    def post(self, request):
        data = request.data

        verify_phone = VerifyPhone.objects.filter(code=data['code']).first()

        if data['code'] != int(verify_phone.code):
            raise exceptions.APIException('Code is incorrect!')

        user = User.objects.filter(phone_number=verify_phone.phone).first()

        if not user:
            raise exceptions.NotFound('User not found!')

        user.is_verified = True
        user.save()
        return Response({
            'message': 'You successfully verified your phone number'
        })
