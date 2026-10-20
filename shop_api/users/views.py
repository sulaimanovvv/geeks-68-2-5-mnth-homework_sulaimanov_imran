from random import randint

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import ConfirmationCode
from .serializers import (
    UserRegisterSerializer,
    UserAuthorizationSerializer,
    UserConfirmSerializer,
)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )

        code = str(randint(100000, 999999))

        while ConfirmationCode.objects.filter(code=code).exists():
            code = str(randint(100000, 999999))

        ConfirmationCode.objects.create(
            user=user,
            code=code
        )

        return Response(
            data={
                'user_id': user.id,
                'confirmation_code': code,
            },
            status=status.HTTP_201_CREATED
        )


class UserAuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            token, created = Token.objects.get_or_create(user=user)

            return Response(data={'token': token.key})

        return Response(
            data='Wrong username or password!',
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserConfirmAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')
        confirmation_code = ConfirmationCode.objects.get(code=code)
        user = confirmation_code.user

        user.is_active = True
        user.save()

        return Response(data={'message': 'User confirmed!'})
