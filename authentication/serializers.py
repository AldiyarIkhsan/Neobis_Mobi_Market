from .models import User
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'birth_date', 'email')

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo', instance.photo)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)

        instance.save()

        return instance

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid', )
    }

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class SendCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance