from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from apps.users.api.serializers import UserSerializer
from apps.users.models import User
from rest_framework.decorators import api_view

# Usando APIView
class UserAPIView(views.APIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many = True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


# Usando el decorador api_view
@api_view(["GET"])
def user_api_view(request):
    if request.method == "GET":
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)
