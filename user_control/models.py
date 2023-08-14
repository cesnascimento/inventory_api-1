from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

Roles = (("admin", "admin"), ("creator", "creator"), ("sale", "sale"))


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if not email:
            raise ValueError("Email field is required")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=8, choices=Roles)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("created_at", )


class UserActivities(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="user_activities", null=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"{self.fullname} {self.action} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class InventoryActivities(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="inventory_activities", null=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    inventario = models.CharField(max_length=255, null=True)
    patrimonio = models.CharField(max_length=255, null=True)
    local = models.CharField(max_length=255, null=True)
    local_novo = models.CharField(max_length=255, null=True)
    colaborador = models.CharField(max_length=255, null=True)
    colaborador_novo = models.CharField(max_length=255, null=True)
    motivo = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"{self.fullname} {self.inventario} {self.patrimonio} {self.local} {self.colaborador} {self.local_novo} {self.colaborador_novo} {self.motivo} on {self.created_at.strftime('%d/%m/%Y')}"

