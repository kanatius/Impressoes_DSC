from django.shortcuts import render
from impressao.models import Impressao
from impressao.forms import ImpressaoForm
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from impressao.repository import ImpressaoRepository

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
    template_name = 'solicitar_impressoes.html'
    success_url='/paciente/listar'


class ImpressaoDelete(DeleteView):
    model = Impressao
    success_url=reverse_lazy('minhas_impressoes')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)