# Views para trabajar con clases APIView
from rest_framework import viewsets

# Serializador y modelo para trabajar con respuestas
from apps.users.api.serializers import UserSerializer

# Auth
from apps.users.authentication_mixin import Authentication

# Usando APIView
class UserAPIView(Authentication, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
