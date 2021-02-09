from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from impressao.service import ImpressaoService

impressaoService = ImpressaoService()

def is_funcionario(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.funcionario:
            return True
    return False

def home(request):

    if is_funcionario(request): #entra na home do cliente caso o usuario logado seja cliente
        impressoes = impressaoService.getImpressoes(request, desc=True)
        return render(request, "home_func.html", context={'impressoes' : impressoes})

    return HttpResponseRedirect("/")