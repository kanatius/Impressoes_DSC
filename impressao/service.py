import os
from .repository import ImpressaoRepository
from .repository import TipoImpressaoRepository
from impressao.forms import ImpressaoForm
from ProjetoDSC.settings import MEDIA_ROOT
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, Http404


def isCliente(request):
    if not request.user.is_anonymous and request.user is not None:
        if request.user.cliente:
            return True
    return False



class ImpressaoService():

    def __init__(self):
        super().__init__()
        self.impressaoRepository = ImpressaoRepository() 

    def getImpressoes(self, request, desc=False):
        if not request.user.is_authenticated:
            return None
            
        if request.user.cliente:
            return self.impressaoRepository.list(cliente_id=request.user.id, desc=desc)
        
        if request.user.funcionario:
            impressoes = self.impressaoRepository.list(imprimida=False, desc=desc)
            
            for impressao in impressoes:
                impressao.visualizado_em = datetime.now() #set visualizado_em nas impressões que foram selecionadas
                impressao.save()
            
            return impressoes


    def getById(self, request, id):
        if not request.user.is_authenticated:
            return None
        
        impressao = self.impressaoRepository.getById(id=id)

        if impressao.cliente.id == request.user.id or request.user.funcionario:
            #se a impressao for do usuario ou se o usuario for cliente
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
        up_data = {}
        
        if request.user.cliente and impressao.imprimida != True: #cliente só pode editar se a impressão ainda não foi imprimida
            
            if "colorida" in data:
                colorida = True if data["colorida"] == 'on' else False
                impressao.colorida = colorida
            else:
                impressao.colorida = False #set False se não vier no formulário

            if 'comentario' in data:
                impressao.comentario = data["comentario"]

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

        if request.user.funcionario:
            #campos que o funcionario pode editar
            # if "vizualizao_em" in data:
            #     impressao.vizualizao_em = data["vizualizao_em"]

            if "imprimida" in data:
                impressao.imprimida : data["imprimida"]
            
            if "prazo_entrega" in data:
                impressao.prazo_entrega : data["prazo_entrega"]
            
            impressao.save()

            return True

        return False
    
    def delete(self, request):

        if isCliente(request):
            impressao = self.impressaoRepository.getById(id=request.POST.get("id_impressao"))

            if impressao is not None:
                if impressao.cliente_id == request.user.id:                   
                    impressao.delete()
                    return True
        
        return False

    #DOWNLOAD FILES
    def download(self, request, path):

        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404