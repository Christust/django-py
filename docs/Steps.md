# Iniciar el proyecto

Creamos un entorno virtual con las siguientes instalaciones:

```
    django = "*"
    djangorestframework = "*"
    django-simple-history = "*"
    pillow = "*"
    python-decouple = "*"
    drf-yasg = "*"
    django-cors-headers = "*"
```

Creamos el proyecto:

```
django-admin startproject <nombre del proyecto>
```

Agregamos las aplicaciones de terceros a nuestras apps instaladas:

```
INSTALLED_APPS = [
    ...,
    "rest_framework",
    "rest_framework.authtoken",
    "simple_history",
    "drf_yasg",
]
```

Agregamos middleware de simple_history:

```
MIDDLEWARE = [
    ...,
    "simple_history.middleware.HistoryRequestMiddleware",
]
```

Agregamos Swagger a nuestro archivo de rutas principal:

```
// urls.py
...
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
...

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="christos.marroquin@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
...

urlpatterns = [
    ...,
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ...,
]
```

Creamos la carpeta apps.
Dentro de ella creamos el archivo "**init**.py", nos posicionamos en ella y creamos la app que administrara los usuarios:

```
django-admin startapp users
```

Asi como en todas las apps creadas en una carpeta modificaremos su apps.py agregando el nombre de la carpeta al string "name", en nuestro caso la carpeta se llama apps:

```
# apps.py

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
```

Creamos el modelo para usuarios junto con su clase manager:

```
# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, ..., password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            ...,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

    def create_user(self, username, ..., password = None, **extra_fields):
        return self._create_user(username, ..., password, False, False, **extra_fields)

    def create_superuser(self, username, ..., password = None, **extra_fields):
        return self._create_user(username, ..., password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("Username", unique=True, max_length=100)
    filed1 = ...
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    historical = HistoricalRecords()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["field1", ...]

    def natural_key(self):
        return (self.username)

    def __str__(self):
        return f"User {self.username}"
```

Agregamos nuestra app a la lista de apps instaladas en settings:

```
INSTALLED_APPS = [
    ...,
    "apps.users",
]
```

Agremos a nuestro settings.py la variable de entorno "AUTH_USER_MODEL" con el valor del modelo de nuestra app que manejara el usuario, antepuesto por el nombre de su app:

```
AUTH_USER_MODEL = "users.User"
```

Ahora podremos correr las migraciones:

```
python manage.py makemigrations
python manage.py migrate
```

En views de la app users Agregaremos las clases para Login y Logout con token:

```
# Para trabajar con sesiones
from django.contrib.sessions.models import Session

# Importamos datetime para manejar tiempos
from datetime import datetime

# Importamos la clase ObtainAuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from apps.users.api.serializers import UserTokenSerializer


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
                        },
                        status.HTTP_201_CREATED,
                    )

                # De no ser creado vamos a cerrar las sesiones de ese usuario
                # Consulamos el modelo session sesiones con expiracion de ahora en adelante
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())

                # Verificamos si existen
                if all_sessions.exists():

                    # Las recorremos
                    for session in all_sessions:
                        # Decodificamos la informacion
                        session_data = session.get_decode()

                        # Verificamos si el id del usuario se empata con el id de la session
                        if user.id == int(session_data.get("_auth_user_id")):

                            # Si es asi la eliminamos
                            session.delete()

                # Borramos el token ya existente y creamos uno nuevo
                token.delete()
                token = Token.objects.create(user=user)

                # Devolvemos el token nuevo
                return Response(
                    {
                        "token": token.key,
                        "user": user_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            # De no ser activo respondemos unauthorized
            return Response("Usuario inactivo", status.HTTP_401_UNAUTHORIZED)

        # Si no es valido el payload respondemos el error
        return Response("No valido", status=status.HTTP_400_BAD_REQUEST)

```

Crearemos una vista para devolver los usuarios registrados. Primero en la app usuarios borramos los archivos views.py y test.py, creamos una carpeta llamada api y dentro de ella cuatro archivos llamados **init**.py, api.py, serializers.py y urls.py.
Dentro de serializers.py colocamos:

```
from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

```

Con esto creamos un serializador sencillo para el modelo User, este nos sirve para convertir a json todos los campos del modelo.

Dentro de api.py colocamos lo siguiente:

```
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.api.serializers import UserSerializer
from apps.users.models import User

class UserApiView(APIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)

```

Con esto creamos una vista que hereda de APIView y devuelve un Response el cual contiene la data del json generado a partir de la consulta del modelo Users, es importante utilizar el parametro many en True si es que es mas de una instancia, si no se usa el serializador pensara que se trata de un solo elemento.

Ahora podremos escribir el archivo urls:

```
from django.urls import path
from apps.users.api.api import UserApiView

urlpatterns = [
    path("usuario/", UserApiView.as_view(), name="usuario_api"),
]
```

El cual enlazaremos a nuestro archivo urls del proyecto:

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("usuario/", include("apps.users.api.urls")),
]
```

Si nosotros usamos las vistas basadas en funciones debemos usar el decorador que nos brinda rest para delimitar que metodos permitiremos en nuestras funciones:

```
...
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

@api_view(["GET", "POST"])
def user_api_view(request):

    if request.method == "GET":
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)
    elif request.method == "POST":
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        else:
            return Response(user_serializer.errors, status=500)
```

## Serializers

Los serializadores se usan para convertir un modelo de Django en JSON y viceversa, dependiendo de como se use.

Un serializador del modelo User se ve asi:

```
from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_email(self, value):
        if "dev" in value:
            raise serializers.ValidationError("El email no puede contener dev")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data["password"])
        update_user.save()
        return update_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "last_name"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "user": instance.username,
            "name": instance.name,
            "last_name": instance.last_name,
        }
```

En este ejemplo uno se utiliza para crear y modificar usuarios, y el otro para enlistar usuarios.

Podemos validar los datos que recibimos con validate_field (siendo filed el atributo que deseamos validar)

El metodo to_representation se usa para que la respuesta tenga la forma que nosotros coloquemos en el return.
