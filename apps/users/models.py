# Importamos models para crear nuestros atributos de nuestro modelo
from django.db import models
# Importamos AbstractBaseUser para crear un modelo personalizado de usuario casi desde 0
# Importamos BaseUserManager para crear un manager para nuestro modelo, el manager
# es el atributo llamado objects que gestiona las funciones create_user por ejemplo
# Importamos PermissionsMixin para heredar a nuestro usuario el mixin de permisos y grupos
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Importamos la clase HistoricalRecords, una app de terceros que lleva un historico de las
# acciones de nuestro modelo
from simple_history.models import HistoricalRecords

# Create your models here.
class UserManager(BaseUserManager):

    # Función base que utilizaran nuestras funciones para crear usuarios normales o superusuario
    def _create_user(self, username: str, email: str, name: str, last_name: str, password: str | None, is_staff: bool, is_superuser: bool, **extra_fields):
        """
        Función base que utilizaran nuestras funciones para crear usuarios normales o superusuario
        """

        # Instanciamos el modelo con los parametros recibidos
        user = self.model(
            username = username,
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )

        # Encriptamos el parametro password y lo depositamos en el atributo password de
        # este usuario
        user.set_password(password)

        # Guardamos el usuario
        user.save(using=self.db)

    # Función para crear usuarios normales
    def create_user(self, username: str, email: str, name: str, last_name: str, password: str | None = None, **extra_fields):
        """
        Función para crear usuarios normales
        """

        # Con los parametros recibidos creamos un usuario normal llamando _create_user
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    # Función para crear superusuarios
    def create_superuser(self, username: str, email: str, name: str, last_name: str, password: str | None = None, **extra_fields):
        """
        Función para crear superusuarios
        """

        # Con los parametros recibidos creamos un superusuario llamando _create_user
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # Atributo principal de nuestro modelo persoanlizado
    username = models.CharField("Username", unique=True, max_length=100)

    # Atributos extra que personalizamos para nuestro modelo
    email = models.EmailField("Email", unique=True, max_length=100)
    name = models.CharField("Name", max_length=100, blank=True, null=True)
    last_name = models.CharField("Lastname", max_length=100, blank=True, null=True)
    image = models.ImageField("Image", upload_to="perfil/", max_length=200, height_field=None, width_field=None, blank=True, null=True)  # type: ignore

    # Atributos requeridos para nuestro mixin de permisos
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Atributo que sera nuestro manager
    objects = UserManager()

    # Atributo necesario para el historial de acciones
    historical = HistoricalRecords()

    # Clase Meta, declaramos aqui nuestro metadatos para el modelo
    class Meta:

        # Atributos para el nombre en singular y el nombre en plural
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Atributos necesarios para un modelo de usuario

    # El atributo USERNAME_FIELD es para delcarar el atributo principal de la clase
    USERNAME_FIELD = "username"
    
    # El atributo REQUIRED_FIELDS se usa para declarar los atributos requeridos al crear un usuario
    REQUIRED_FIELDS = ["email", "name", "last_name"]

    # Función para declarar la llave natural del modelo, si hay relaciones uno a muchos o muchos
    # a muchos, en lugar de mostrar el id, mostrara lo que esta función nos retorne
    def natural_key(self):
        return (self.username)

    # Función para retornar un string al llamar una instancia de este modelo 
    def __str__(self):
        return f"User {self.username}"
