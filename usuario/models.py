from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    funcionario = models.BooleanField("funcionario", null=True, blank=True)
    cliente = models.BooleanField("cliente", null=True, blank=True)
