from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from impressao.service import ImpressaoService
from .forms import RelatorioForm
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from datetime import datetime

from xhtml2pdf import pisa

impressaoService = ImpressaoService()

def is_funcionario(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.funcionario:
            return True
    return False

def home(request):

    if is_funcionario(request) or request.user.funcionario_aluno: #entra na home do funcionario caso o usuario logado seja funcionario
        impressoes = impressaoService.getImpressoes(request, desc=False)
        return render(request, "home_func.html", context={'impressoes' : impressoes})

    return HttpResponseRedirect("/")


def relatorio_page(request):

    if is_funcionario(request):
        return render(request, "relatorio_page.html", context={"form" : RelatorioForm()})
    
    return HttpResponseRedirect(request, "/")



def gerar_relatorio(request):

    if not is_funcionario(request):
        return HttpResponseRedirect(request, "/")

    form = RelatorioForm(request.GET)

    if not form.is_valid:
        return redirect("usuario:gerar_relatorio", context= {
            "form" : form
        })

    data_inicio = datetime.strptime(request.GET["data_inicio"], "%d/%m/%Y")
    data_inicio = data_inicio.replace(hour=0, minute=0)
    data_fim = datetime.strptime(request.GET["data_fim"], "%d/%m/%Y")
    data_fim = data_fim.replace(hour=23, minute=59, second=59)

    turma_id = None

    if request.GET["turma"]:
        turma_id = request.GET["turma"]

    dados = impressaoService.getReportData(
        request=request, 
        cliente_id=(request.GET["cliente"]), 
        turma_id=turma_id, 
        data_inicio=data_inicio, 
        data_fim=data_fim)

    template = get_template("relatorio.html")
    html  = template.render({
        "teste" : "kasmdklams",
        "data_inicio" : data_inicio.strftime("%d/%m/%Y"),
        "data_fim" : data_fim.strftime("%d/%m/%Y"),
        "impressoes" : dados["impressoes"],
        "total_laudas" : dados["total_laudas"],
        "cliente_nome" : dados["cliente_nome"],
        "turma_nome" : dados["turma_nome"]
        })
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    
    return HttpResponseRedirect(request, "/")
