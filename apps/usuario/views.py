from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
#usuario
from .forms import CreateUserForm
from django.views.generic.edit import CreateView

# Create your views here.
def login(request):
    if request.method == "POST":

        email = request.POST["email"]
        senha = request.POST["password"]
        
        usuario = authenticate(request, email=email, password=senha)
        
        if usuario:
            print("login efetuado com sucesso!")
            django_login(request, usuario)

        return redirect("/")


@login_required       
def logout(request):
    django_logout(request)
    return HttpResponseRedirect("/")



class CreateUser(CreateView):
    model = Usuario
    form_class = CreateUserForm
    template_name = 'accounts/new-user.html'
    success_url = "/"
    success_message = "Cadastrado com sucesso"