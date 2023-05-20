# Views para trabajar con clases APIView
from rest_framework import viewsets

# Serializador y modelo para trabajar con respuestas
from apps.users.api.serializers import UserSerializer

# Usando APIView
class UserAPIView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
