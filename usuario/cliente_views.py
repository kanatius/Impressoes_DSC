from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from impressao.forms import ImpressaoForm
from impressao.models import Impressao
from usuario.models import Usuario
from django.contrib import messages
from django.core.paginator import Paginator

from impressao.service import ImpressaoService


impressaoService = ImpressaoService()


def isFuncionario(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.funcionario:
            return True
    return False

def isCliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False

#Acessar home cliente
def home(request):
    if isCliente(request): #entra na home do cliente caso o usuario logado seja cliente

        page = 1

        if 'page' in request.GET:
            page = int(request.GET.get('page'))
        
        impressoes = impressaoService.getImpressoes(request, desc=True)
        paginator = Paginator(impressoes, 8)
        page_obj = paginator.page(page) 

        return render(request, "minhas_impressoes.html", context={"page_obj" : page_obj})

    return HttpResponseRedirect("/")

def solicitar_impressao(request):
    if request.method == "GET":
        if isCliente(request):
            return render(request, "solicitar_impressao.html", context={'form' : ImpressaoForm()})
    
    elif request.method == "POST":
        
        if impressaoService.create(request=request):
            messages.success(request, 'Impressão cadastrada com sucesso!')

            return redirect("usuario:minhas_impressoes")

        return render(request, "solicitar_impressao.html", context={'form' : ImpressaoForm()})
                
    return HttpResponseRedirect("/")

def update_impressao(request, id_impressao):

    if request.method == "GET":
        impressao = impressaoService.getById(request, id_impressao)
        
        if impressao is None:
            return HttpResponseRedirect("/")

        form = ImpressaoForm(instance=impressao)
        return render(request, "edit_impressao.html", context={"form" : form})

    if request.method == "POST":
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")

        if impressaoService.update(request=request ,id=id_impressao):
            
            if isCliente(request) :
                messages.success(request, "Impressão editada com sucesso")
                return redirect("usuario:minhas_impressoes")
            
            if isFuncionario(request):
                messages.success(request, "Informações atualizadas com sucesso")
                return redirect("usuario:home_func")
        else:
            messages.error(request, "Não foi possível editar a impressão")

            if isCliente(request):
                return redirect("usuario:minhas_impressoes")
            
            if isFuncionario(request):
                return redirect("usuario:home_func")
        



def delete_impressao(request):
    if request.method == "POST":

        if ImpressaoService().delete(request=request, id=request.POST.get("id_impressao")):
                    
            messages.success(request, "Impressao removida com sucesso!")
            
            return redirect("usuario:minhas_impressoes")
            
            
        messages.success(request, "Erro na solicitação")
        return redirect("usuario:minhas_impressoes")
    
    return HttpResponseRedirect("/")