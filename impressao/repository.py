from .models import Impressao, TipoImpressao

#IMPRESSÃO REPOSITORY

class ImpressaoRepository:

    
    def list(self, imprimida=None, cliente_id=None, order_by='id', desc=False):
        query = Impressao.objects.all()

        if imprimida is not None:
            query = query.filter(imprimida=imprimida)

        if cliente_id is not None:
            query = query.filter(cliente_id=cliente_id)

        query = query.order_by(order_by)

        if desc :
            query = query.reverse()
        
        return query
    
    def getById(self, id):
        try:
            return Impressao.objects.get(id=id)
        except:
            return None

class TipoImpressaoRepository:

    def getAll(self):
        return TipoImpressao.objects.all()

    def getById(self, id=None):
        try:
            return TipoImpressao.objects.get(id=id)
        except:
            return None