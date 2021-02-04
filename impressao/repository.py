from .models import Impressao, TipoImpressao

#IMPRESSÃO REPOSITORY

class ImpressaoRepository:

    
    def list(self, imprimida=None, cliente_id=None):
        query = Impressao.objects.all()

        if imprimida is not None:
            query = query.filter(imprimida=imprimida)

        if cliente_id is not None:
            query = query.filter(cliente_id=cliente_id)

        return query
    
    def getById(self, request):
        if request.user.is_authenticated :
            return Impressao.objects.filter(cliente_id=request.user.id)
        
        return []

class TipoImpressaoRepository:

    def getAll(self):
        return TipoImpressao.objects.all()
