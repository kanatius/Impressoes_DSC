from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from impressao.forms import ImpressaoForm
from impressao.models import Impressao
from usuario.models import Usuario
from django.contrib import messages

from impressao.repository import ImpressaoRepository


def isCliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False


def home(request):
    if isCliente(request): #entra na home do cliente caso o usuario logado seja cliente
        impressoes = ImpressaoRepository().list(cliente_id=request.user.id, desc=True)
        return render(request, "minhas_impressoes.html", context={"impressoes": impressoes})

    return HttpResponseRedirect("/")

def solicitar_impressao(request):
    if request.method == "GET":
        if isCliente(request):
            return render(request, "solicitar_impressao.html", context={'form' : ImpressaoForm()})
    
    elif request.method == "POST":
        if isCliente(request):
            form = ImpressaoForm(request.POST, files=request.FILES)
            if form.is_valid():
                impressao = form.save(commit=False)
                impressao.cliente = request.user
                impressao.save()                

                messages.success(request, 'Impressão cadastrada com sucesso!')

                return redirect("usuario:minhas_impressoes")

        return render(request, "solicitar_impressao.html", context={'form' : ImpressaoForm()})
                


    return HttpResponseRedirect("/")