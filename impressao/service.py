import os

from impressao.repository import ImpressaoRepository
from impressao.repository import TipoImpressaoRepository
from impressao.repository import TurmaRepository

from impressao.forms import ImpressaoForm

from ProjetoDSC.settings import MEDIA_ROOT

from datetime import datetime

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.mail import send_mail
from ProjetoDSC.email_data import EMAIL_HOST_USER


def isCliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False

def isFuncionario(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.funcionario:
            return True
    return False


class ImpressaoService():

    def __init__(self):
        super().__init__()
        self.impressaoRepository = ImpressaoRepository() 
        self.tipoRepository = TipoImpressaoRepository()
        self.turmaRepository = TurmaRepository()

    def getImpressoes(self, request, offset=0, limit=0, desc=False):
        if not request.user.is_authenticated:
            return None
            
        if isCliente(request):
            return self.impressaoRepository.list(cliente_id=request.user.id, offset=offset, limit=limit, desc=desc)

        if isFuncionario(request) or request.user.funcionario_aluno:
            
            impressoes = self.impressaoRepository.list(imprimida=False, desc=desc)

            if request.user.funcionario_aluno: #se o funcionario for aluno
                
                prova = self.tipoRepository.getByNameEquals("Prova")
                teste = self.tipoRepository.getByNameEquals("Teste")

                impressoes = impressoes.filter(~Q(tipo=prova)) #remove Provas
                impressoes = impressoes.filter(~Q(tipo=teste)) #remove Testes

            for impressao in impressoes:
                impressao.visualizado_em = datetime.now() #set visualizado_em nas impressões que foram selecionadas
                impressao.save()
            
            return impressoes


    def getById(self, request, id):
        if not request.user.is_authenticated:
            return None
        
        impressao = self.impressaoRepository.getById(id=id)
        
        if impressao is None:
            return None

        if impressao.cliente.id == request.user.id or request.user.funcionario:
            #se a impressao for do usuario ou se o usuario for cliente
            if request.user.funcionario_aluno and (impressao.tipo.nome.lower() == "prova" or impressao.tipo.nome.lower == "teste"):
                return None #se o usuario for aluno e impressao for prova ou teste, retorna None

            #retorna impressao se:
            #1 - usuario logado for funcionario
            #2 - se o funcionario for aluno e a impressao não for prova ou teste
            #3 - se o usuario for cliente e a impressao for dele
            return impressao
        
        return None
    
    def create(self, request):
        if isCliente(request):
            form = ImpressaoForm(request.POST, files=request.FILES)
            if form.is_valid():
                impressao = form.save(commit=False)
                impressao.cliente = request.user
                impressao.save()
                return True
        return False
    
    def update(self, request, id=None):

        if id is None:
            return None
        
        if not request.user.is_authenticated:
            return None

        impressao = self.impressaoRepository.getById(id=id)
        
        if impressao is None:
            return None
    
        data = request.POST

        if request.user.cliente and impressao.imprimida != True: #cliente só pode editar se a impressão ainda não foi imprimida
            
            if "colorida" in data:
                colorida = True if data["colorida"] == 'on' else False
                impressao.colorida = colorida
            else:
                impressao.colorida = False #set False se não vier no formulário

            if 'comentario' in data:
                impressao.comentario = data["comentario"]
            
            if 'turma' in data:
                turma = self.turmaRepository.getById(data["turma"])
                print(turma)
                impressao.turma = turma
                

            if request.FILES.get("uri_arquivo"):

                file = request.FILES.get("uri_arquivo")
                default_storage.delete(str(impressao.uri_arquivo)) #delete old file
                path = default_storage.save(file.name, ContentFile(file.read())) #save file in default dir
                impressao.uri_arquivo = path #set file
                

            if 'qtd_copias' in data:
                impressao.qtd_copias = data["qtd_copias"]

            
            if 'tipo' in data:
                impressao.tipo = TipoImpressaoRepository().getById(id=int(data["tipo"]))

            # UPDATE FILE
            
            impressao.save()

            return True

        #Não está sendo usado
        # if request.user.funcionario:
        #     #campos que o funcionario pode editar
        #     # if "vizualizao_em" in data:
        #     #     impressao.vizualizao_em = data["vizualizao_em"]

        #     if "imprimida" in data:
        #         impressao.imprimida : data["imprimida"]
            
        #     if "prazo_entrega" in data:
        #         impressao.prazo_entrega : data["prazo_entrega"]
            
        #     impressao.save()

        #     return True

        return False
    
    def setImprimida(self, request):
        if not request.user.is_authenticated:
            return False

        if not isFuncionario(request) and not request.user.funcionario_aluno:
            return False
    
        impressao = self.impressaoRepository.getById(request.POST.get("id_impressao"))

        if impressao is None:
            return False
        
        prova = self.tipoRepository.getByNameEquals("Prova")
        teste = self.tipoRepository.getByNameEquals("Teste")

        if request.user.funcionario_aluno and (impressao.tipo == prova or impressao.tipo == teste):
            return False #retorna false se a impressão for prova ou teste e o funcionario for aluno

        impressao.imprimida = True
        impressao.set_imprimida_em = datetime.now()
        # impressao.save()

        # send_mail(
        #     'Sua Impressão está pronta!',
        #     'Olá ' + request.user.getFullName() + ", sua impressão : " + impressao.uri_arquivo.name + " está pronta!",
        #     EMAIL_HOST_USER,
        #     ['natankwo@gmail.com'],
        #     fail_silently=False,
        # )

        return True

    def delete(self, request):

        if isCliente(request):
            impressao = self.impressaoRepository.getById(id=request.POST.get("id_impressao"))

            if impressao is not None:
                if impressao.cliente_id == request.user.id and not impressao.imprimida:
                    default_storage.delete(str(impressao.uri_arquivo)) #delete old file                   
                    impressao.delete()
                    return True
        
        return False

    #DOWNLOAD FILES
    def download(self, request, path):
        
        if not request.user.is_authenticated:
            raise Http404  #retorna erro se o usuário não estiver autenticado
        
        impressao = self.impressaoRepository.getByPath(path)

        #----- NÃO MUDE SE NÃO SOUBER O QUE ESTÁ FAZENDO -----#

        if impressao is None:
            raise Http404 #retorna erro se a impressao não existe

        if not isCliente(request) and not isFuncionario(request) and not request.user.funcionario_aluno:
            raise Http404 #retorna erro se não for funcionário, cliente ou funcionario aluno

        if (isCliente(request) and impressao.cliente.id != request.user.id) and not isFuncionario(request):
            raise Http404 #retorna erro se o cliente não for dono da impressao e tbm não é funcionario
        
        prova = self.tipoRepository.getByNameEquals("Prova")
        teste = self.tipoRepository.getByNameEquals("Teste")


        if request.user.funcionario_aluno and (impressao.tipo == prova or impressao.tipo == teste):
            raise Http404 #retorna erro se o funcionario aluno tentar baixar uma prova ou teste
        #----- NÃO MUDE SE NÃO SOUBER O QUE ESTÁ FAZENDO -----#

        
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/default")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404