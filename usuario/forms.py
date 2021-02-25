from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Usuario
from .repository import UsuarioRepository
from impressao.repository import TurmaRepository


usuarioRepository = UsuarioRepository()
turmaRepository = TurmaRepository()

class CreateUserForm(UserCreationForm):

    class Meta:
        model: Usuario

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]

        if commit:
            user.save()

        return user

class ChangeUserForm(UserChangeForm):

    class Meta:
        model: Usuario

    def save(self, commit=True):
        user = super().save(commit=False)
        # user.set_password(self.clean("password1"))
        user.email = self.cleaned_data["email"]
        user.funcionario= self.cleaned_data["funcionario"]
        user.cliente = self.cleaned_data["cliente"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]


        if commit:
            user.save()

        return user



class RelatorioForm(forms.Form):

    cliente = forms.ModelChoiceField(usuarioRepository.getClientes(), required=True)
    turma = forms.ModelChoiceField(turmaRepository.getAll(), required=False)
    data_inicio = forms.DateField(required=True)
    data_fim = forms.DateField(required=True)
