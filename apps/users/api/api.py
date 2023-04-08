# Views para trabajar con clases APIView
from rest_framework import views

# Status para indicar el estatus de la respuesta
from rest_framework import status

# Response para devolver una respuesta http
from rest_framework.response import Response

# Serializador y modelo para trabajar con respuestas
from apps.users.api.serializers import UserSerializer, UserListSerializer
from apps.users.models import User

# Decorador para trabajar con funciones
from rest_framework.decorators import api_view


# Usando APIView
class UserAPIView(views.APIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


# Usando el decorador api_view
@api_view(["GET", "POST"])
def user_api_view(request):
    if request.method == "GET":
        users = User.objects.all()
        user_serializer = UserListSerializer(users, many=True)
        return Response(user_serializer.data)
    if request.method == "POST":
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def user_detail_view(request, pk=None):
    if request.method == "GET":
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    elif request.method == "PUT":
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)

    elif request.method == "DELETE":
        user = User.objects.filter(id=pk).first()
        user.delete()
        return Response("Eliminado")
