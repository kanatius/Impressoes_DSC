from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from impressao.repository import ImpressaoRepository


def isCliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False


def home(request):
    if isCliente(request): #entra na home do cliente caso o usuario logado seja cliente
        impressoes = ImpressaoRepository().getImpressoesDoClienteLogado(request)
        return render(request, "home_cliente.html", context={"impressoes": impressoes})

    return HttpResponseRedirect("/")

def solicitar_impressao(request):
    if isCliente(request):
        return render(request, "solicitar_impressao.html")
    
    return HttpResponseRedirect("/")