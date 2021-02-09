from django.shortcuts import render
from impressao.models import Impressao
from impressao.forms import ImpressaoForm
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from impressao.repository import ImpressaoRepository
from django.contrib import messages
from .service import ImpressaoService
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


impressaoService = ImpressaoService()


def downloadFile(request, filename):
    return impressaoService.download(request, filename)

def setImprimida(request):
    if request.method == "POST":
        response = impressaoService.setImprimida(request=request)
        if response:
            messages.success(request, "Impressão definida como imprimida com sucesso!<br>O cliente já consegue visualizar a modificação.")
            return redirect("usuario:home_funcionario")
    else:
        return HttpResponseRedirect("/")

# Create your views here.
class ImpressaoCreate(CreateView):
    model = Impressao
    form_class = ImpressaoForm
    template_name = 'solicitar_impressao.html'

    def get_context_data(self, **kwargs):
        data = super(ImpressaoCreate, self).get_context_data(**kwargs)
        return data

    def get_success_url(self):
        return reverse_lazy('minhas_impressoes')

class ImpressaoList(ListView):

    model = Impressao
    template_name = 'minhas_impressoes.html'  # Specify your own template name/location

    def get_queryset(self):
        impressoes = ImpressaoRepository().list(cliente_id= self.request.user.id)
        print(impressoes)
        return impressoes

class ImpressaoUpdate(UpdateView):
    ## implementacao da regra de negocio
    model = Impressao
    form_class = ImpressaoForm
    template_name = 'edit_impressao.html'
    # success_message = 'Impressão editada com sucesso!'
    success_url='/usuario/cliente/impressao/list'

    # def save_model(self, request, obj, form, change):
    #     super(ImpressaoUpdate, self).save_model(request, obj, form, change)
    #     if obj.status == "OK":
    #         messages.success(request, "Impressão editada com sucesso!")
    #     elif obj.status == "NO":
    #         messages.error(request, "Erro ao Editar")

class ImpressaoDelete(DeleteView):
    model = Impressao
    success_url=reverse_lazy('minhas_impressoes')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)