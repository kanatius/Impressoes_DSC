from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from impressao.forms import ImpressaoForm
from impressao.models import Impressao
from usuario.models import Usuario
from django.contrib import messages

from impressao.service import ImpressaoService


def isCliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False

#Acessar home cliente
def home(request):
    if isCliente(request): #entra na home do cliente caso o usuario logado seja cliente
        impressoes = ImpressaoService().getImpressoes(request, desc=False)
        return render(request, "minhas_impressoes.html", context={"impressoes": impressoes})

    return HttpResponseRedirect("/")

def solicitar_impressao(request):
    if request.method == "GET":
        if isCliente(request):
            return render(request, "solicitar_impressao.html", context={'form' : ImpressaoForm()})
    
    elif request.method == "POST":
        
        if ImpressaoService().create(request=request):
            messages.success(request, 'Impressão cadastrada com sucesso!')

            return redirect("usuario:minhas_impressoes")

        return render(request, "solicitar_impressao.html", context={'form' : ImpressaoForm()})
                
    return HttpResponseRedirect("/")


def delete_impressao(request):
    if request.method == "POST":

        if ImpressaoService().delete(request=request):
                    
            messages.success(request, "Impressao removida com sucesso!")
            
            return redirect("usuario:minhas_impressoes")
            
            
        messages.success(request, "Erro na solicitação")
        return redirect("usuario:minhas_impressoes")
    
    return HttpResponseRedirect("/")