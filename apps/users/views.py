# Para trabajar con sesiones
from django.contrib.sessions.models import Session

# Importamos datetime para manejar tiempos
from datetime import datetime

# Importamos la clase ObtainAuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.users.api.serializers import UserTokenSerializer


def delete_sessions(user):
    # Funcion para eliminar sesiones
    # De no ser creado vamos a cerrar las sesiones de ese usuario
    # Consultamos el modelo session sesiones con expiracion de ahora en adelante
    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())

    # Verificamos si existen
    if all_sessions.exists():
        # Las recorremos
        for session in all_sessions:
            # Decodificamos la informacion
            session_data = session.get_decoded()

            # Verificamos si el id del usuario se empata con el id de la session
            if user.id == int(session_data.get("_auth_user_id")):
                # Si es asi la eliminamos
                session.delete()


class UserToken(APIView):
    def get(self, request):
        username = request.GET.get("username")
        try:
            user_token = Token.objects.get(
                user=UserTokenSerializer.Meta.model.objects.filter(
                    username=username
                ).first()
            )
            return Response({"token": user_token.key})
        except:
            return Response(
                {"error": "Credenciales incorrectas"}, status.HTTP_400_BAD_REQUEST
            )


# Creeamos la clase Login la cual hereda de ObtainAuthToken
class Login(ObtainAuthToken):
    def post(self, request):
        # La clase ObtainAuthToken ya cuenta con serializer el cual solo tiene un campo user y uno password
        login_serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        # Verificamos si es valido el payload recibido
        if login_serializer.is_valid():
            # De ser valido depositamos el user devuelto por el serializador
            user = login_serializer.validated_data["user"]

            # Verificamos si es un usuario activo
            if user.is_active:
                # De ser un usuario activo consultamos o  generamos el Token
                # La funcion get_or_create devuelve la instancia y si fue creada o no. De no existir la crea.
                # El modelo Token recibe al usuario solamente
                token, created = Token.objects.get_or_create(user=user)

                # Serializamos el usuario para retornarlo
                user_serializer = UserTokenSerializer(user)
                # Si el token fue creado respondemos el token y el usuario unicamente
                if created:
                    return Response(
                        {
                            "token": token.key,
                            "user": user_serializer.data,
                            "created": created,
                        },
                        status.HTTP_201_CREATED,
                    )

                delete_sessions(user)

                # Borramos el token ya existente y creamos uno nuevo
                token.delete()
                token = Token.objects.create(user=user)

                # Devolvemos el token nuevo
                return Response(
                    {
                        "token": token.key,
                        "user": user_serializer.data,
                        "created": False,
                    },
                    status=status.HTTP_200_OK,
                )

            # De no ser activo respondemos unauthorized
            return Response("Usuario inactivo", status.HTTP_401_UNAUTHORIZED)

        # Si no es valido el payload respondemos el error
        return Response(
            {"message": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST
        )


class Logout(APIView):
    def post(self, request):
        try:
            token = request.data["token"]
            token = Token.objects.filter(key=token).first()
            if token:
                user = token.user
                delete_sessions(user)
                session_message = "Sesiones eliminadas"

                # Borramos el token ya existente y creamos uno nuevo
                token.delete()
                token_message = "Token eliminado"

                return Response(
                    {"token_message": token_message, "session_message": session_message}
                )

            return Response("No se encontro usuario", status.HTTP_400_BAD_REQUEST)
        except:
            return Response("No se envio token", status.HTTP_400_BAD_REQUEST)
