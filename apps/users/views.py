from datetime import datetime

from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.api.serializers import CustomTokenObtainPairSerializer, UserSerializer
from apps.users.models import User


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    "token": login_serializer.validated_data["access"],
                    "refresh_token":login_serializer.validated_data["refresh"],
                    "user":user_serializer.data
                }, status=status.HTTP_200_OK)
        return Response({"error": "Usuario o contraseña incorrectos"}, status.HTTP_400_BAD_REQUEST)
    
class Logout(GenericAPIView):
    def post(self, request):
        user = User.objects.filter(id=request.data.get("user", "")).first()
        if user:
            RefreshToken.for_user(user)
            return Response({
                "message": "Sesion cerrada correctamente"
            }, status.HTTP_200_OK)
        return Response({"error": "Usuario inexistente"}, status.HTTP_400_BAD_REQUEST)