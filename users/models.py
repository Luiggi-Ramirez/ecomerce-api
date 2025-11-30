from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class CustomBaseUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Falta correo")
        email = self.normalize_email(email)
        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe ser staff")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El usuario tiene que ser superuser")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=1, unique=False, null=True, blank=True)
    email = models.EmailField("Email", max_length=120, unique=True, db_index=True)
    first_name = models.CharField("Nombre", max_length=120)
    last_name = models.CharField("Apellido", max_length=120)
    phone = models.CharField("Teléfono", max_length=12, null=True, blank=True)
    image = models.CharField("Link Image", max_length=255, null=True, blank=True)
    notification_token = models.CharField(
        "Token Notificaciones", max_length=255, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
