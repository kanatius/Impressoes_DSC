from .repository import ImpressaoRepository
from impressao.forms import ImpressaoForm

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
            return self.impressaoRepository.list(imprimida=False, desc=desc)

    def getById(self, request, id):
        if not request.user.is_authenticated:
            return None
        
        impressao = self.impressaoRepository.getById(id=id)

        if impressao.cliente.id == request.user.id or request.user.funcionario:
            #se a impressao for do usuario ou se o usuario for cliente
            return impressao
        
        return None
    
    def create(self, request):
        if isCliente:
            form = ImpressaoForm(request.POST, files=request.FILES)
            if form.is_valid():
                impressao = form.save(commit=False)
                impressao.cliente = request.user
                impressao.save()
                return True
        return False
    
    
    def delete(self, request):

        if isCliente(request):
            impressao = self.impressaoRepository.getById(id=request.POST.get("id_impressao"))

            # print("id impressao: " + str(request.POST.get("id_impressao")))
            # print(impressao)

            if impressao is not None:
                if impressao.cliente_id == request.user.id:                   
                    impressao.delete()
                    return True
        
        return False