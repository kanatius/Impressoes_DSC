from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Usuario


class CreateUserForm(UserCreationForm):

    class Meta:
        model: Usuario

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.funcionario= self.cleaned_data["funcionario"]
        user.cliente = self.cleaned_data["cliente"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]


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