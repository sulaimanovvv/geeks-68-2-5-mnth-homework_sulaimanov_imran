from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ConfirmationCode


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User already exists!')

        return username


class UserAuthorizationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class UserConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_code(self, code):
        if not ConfirmationCode.objects.filter(code=code).exists():
            raise serializers.ValidationError('Invalid confirmation code!')

        return code
