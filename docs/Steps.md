# Iniciar el proyecto

Creamos un entorno virtual con las siguientes instalaciones:
```
    django = "*"
    djangorestframework = "*"
    django-simple-history = "*"
    pillow = "*"
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
    "simple_history",
]
```

Agregamos middleware de simple_history:
```
MIDDLEWARE = [
    ...,
    "simple_history.middleware.HistoryRequestMiddleware",
]
```

Creamos la carpeta apps.
Dentro de ella creamos el archivo "__init__.py", nos posicionamos en ella y creamos la app que administrara los usuarios:
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

Crearemos una vista para devolver los usuarios registrados. Primero en la app usuarios borramos los archivos views.py y test.py, creamos una carpeta llamada api y dentro de ella cuatro archivos llamados __init__.py, api.py, serializers.py y urls.py.
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
