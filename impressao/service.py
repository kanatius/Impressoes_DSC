import os

from impressao.repository import ImpressaoRepository, TipoImpressaoRepository, TurmaRepository
from usuario.repository import UsuarioRepository

from impressao.forms import ImpressaoForm

from ProjetoDSC.settings import MEDIA_ROOT

from datetime import datetime

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.mail import send_mail
from ProjetoDSC.settings import EMAIL_HOST_USER


def isCliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False

def isFuncionario(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.funcionario or request.user.funcionario_aluno:
            return True
    return False


class ImpressaoService():

    def __init__(self):
        super().__init__()
        self.impressaoRepository = ImpressaoRepository() 
        self.tipoRepository = TipoImpressaoRepository()
        self.turmaRepository = TurmaRepository()
        self.usuarioRepository = UsuarioRepository()

    def getImpressoes(self, request, offset=0, limit=0, desc=False):
        if not request.user.is_authenticated:
            return None
            
        if isCliente(request):
            return self.impressaoRepository.list(cliente_id=request.user.id, offset=offset, limit=limit, desc=desc)

        if isFuncionario(request) or request.user.funcionario_aluno:
            impressoes = []

            if request.user.funcionario_aluno:
                #se o funcionario for aluno, retira as provas e testes
                prova = self.tipoRepository.getByNameEquals("Prova")
                teste = self.tipoRepository.getByNameEquals("Teste")
                impressoes = self.impressaoRepository.list(imprimida=False, desc=desc, no_tipo=[prova, teste])
            else:
                impressoes = self.impressaoRepository.list(imprimida=False, desc=desc)
                
        
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
                print("Formulário válido")
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
        
        request_from = ""

        try: #for api
            data = request.data
            request_from = "api"
        except: #for form
            data = request.POST
            request_from = "website"

        if request.user.cliente and impressao.imprimida != True: #cliente só pode editar se a impressão ainda não foi imprimida
            
            if "colorida" in data:
                colorida = True if (data["colorida"] == 'on' or data["colorida"] == 'true') else False
                impressao.colorida = colorida
            elif request_from == "website":
                #se não vier no form e vier do website

                #se a requisição vier do website, o campo "colorida" não vem com o form caso não estiver marcado
                #se não vier com o form é pq é False
                impressao.colorida = False
            
            if 'comentario' in data:
                impressao.comentario = data["comentario"]
            
            if 'turma' in data:
                turma = self.turmaRepository.getById(data["turma"])
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

        impressao.qtd_laudas_imprimidas = int(request.POST.get("qtd_laudas_imprimidas"))

        impressao.save()

        # send_mail(
        #     'Sua Impressão está pronta!',
        #     'Olá ' + impressao.cliente.getFullName() + ", sua impressão : cod-" + str(impressao.id) + " " + impressao.uri_arquivo.name + " está pronta!",
        #     EMAIL_HOST_USER,
        #     [impressao.cliente.email],
        #     fail_silently=False,
        # )

        return True

    def delete(self, request, id):

        if isCliente(request):

            impressao = self.impressaoRepository.getById(id=id)

            if impressao is not None:
                if impressao.cliente_id == request.user.id and not impressao.imprimida:
                    #se a impressao for do cliente e ainda não foi imprimida
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

    def getReportData(self, request, cliente_id, data_inicio, data_fim, turma_id=None):

        if not isFuncionario(request):
            return None
        
        cliente_nome = self.usuarioRepository.getById(cliente_id).getFullName()

        impressoes = self.impressaoRepository.list(
            imprimida=True, 
            cliente_id=cliente_id, 
            order_by="set_imprimida_em",
            imprimida_min_date= data_inicio,
            imprimida_max_date= data_fim,
            turma_id= turma_id
            )
        
        turma_nome = ""

        if turma_id is not None:
            turma_nome = self.turmaRepository.getById(turma_id)
        else:
            turma_nome = "Todas"

        total_laudas = 0

        for impressao in impressoes:
            total_laudas += impressao.qtd_laudas_imprimidas

        return {
            "cliente_nome" : cliente_nome,
            "impressoes" : impressoes,
            "total_laudas" : total_laudas,
            "turma_nome" : turma_nome
            }


class TipoImpressaoService:

    def __init__(self):
        super().__init__()
        self.tipoImpressaoRepository = TipoImpressaoRepository()
    
    def getAllTipos(self, request):
        return self.tipoImpressaoRepository.getAll()


class TurmaService:

    def __init__(self):
        super().__init__()
        self.turmaRepository = TurmaRepository()
    
    def getById(self, request, id):
        return self.turmaRepository.getById(id)

    def getAllTurmas(self, request):
        return self.turmaRepository.getAll()
