from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')
        return self._create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField("email", unique=True)
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS

    funcionario = models.BooleanField("funcionario", null=True, blank=True)
    funcionario_aluno = models.BooleanField("funcionario_aluno", null=True, blank=True)
    cliente = models.BooleanField("cliente", null=True, blank=True)

    def __str__(self):
        return super().first_name + " " + super().last_name
    
    def getFullName(self):
        return super().first_name + " " + super().last_name
        
    objects = UsuarioManager()