from .models import Impressao, TipoImpressao

#IMPRESSÃO REPOSITORY

class ImpressaoRepository:

    def getImpressoesDoClienteLogado(self, request):
        if request.user.is_authenticated :
            return Impressao.objects.filter(cliente_id=request.user.id)
        
        return []
