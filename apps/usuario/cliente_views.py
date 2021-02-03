from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


def is_cliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False


def home(request):
    print(123123)
    if is_cliente(request): #entra na home do cliente caso o usuario logado seja cliente
        return render(request, "home_cliente.html")

    return HttpResponseRedirect("/")
