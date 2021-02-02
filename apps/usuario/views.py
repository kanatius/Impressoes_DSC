from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
#usuario

# Create your views here.
def login(request):
    if request.method == "POST":

        email = request.POST["email"]
        senha = request.POST["senha"]
        
        usuario = authenticate(request, email=email, password=senha)

        if usuario:
            return render(request, "login_efetuado.html")

        return redirect("/")


        # try:
        #     usuario = Usuario.objects.get(email=email)
        # except Usuario.DoesNotExist:
        #     usuario = None
        # else:
        #     print(usuario)
        #     if check_password(usuario, senha):
        #         print("senha correta")
        #         login(request, usuario)
        #         #redireciona para a tela de ogin efetuado caso consiga logar
        #         
            
    


@login_required
def logout(request):
    logout(request)
    return redirect('')