from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.decorators import login_required
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

        if usuario is not None:
            if usuario.funcionario or usuario.cliente or usuario.funcionario_aluno:
                django_login(request, usuario)
                if usuario.funcionario or usuario.funcionario_aluno:
                    return redirect("usuario:home_funcionario")
                if usuario.cliente:
                    return redirect("usuario:minhas_impressoes")

        return HttpResponseRedirect("/")


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