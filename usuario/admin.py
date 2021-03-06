from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import *

# Register your models here.
UserAdmin.fieldsets += ('Perfil de acesso', {'fields': ('cliente', 'funcionario', 'funcionario_aluno')}),

class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm
    model = Usuario
    list_display = ['username', "cliente", "funcionario", "funcionario_aluno", "first_name", "last_name"]
    # readonly_fields = ['password']

admin.site.register(Usuario, CustomUserAdmin)