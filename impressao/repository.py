from .models import Impressao, TipoImpressao, Turma

#IMPRESSÃO REPOSITORY

class ImpressaoRepository:

    
    def list(self, imprimida=None, cliente_id=None, order_by='id', limit=0, offset=0, desc=False):
        query = Impressao.objects.all()

        if imprimida is not None:
            query = query.filter(imprimida=imprimida)

        if cliente_id is not None:
            query = query.filter(cliente_id=cliente_id)

        query = query.order_by(order_by)

        if limit == 0:
            limit = len(query)

        if desc :
            query = query.reverse()[offset:(offset+limit)]
        else:
            query = query[offset:(offset+limit)]

        return query
    
    def getById(self, id):
        try:
            return Impressao.objects.get(id=id)
        except:
            return None

    def getByPath(self, path):
        try:
            return Impressao.objects.get(uri_arquivo=path)
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
    
    def getByNameEquals(self, name):
        try:
            return TipoImpressao.objects.get(nome=name)
        except:
            None

class TurmaRepository:
    
    def getById(self, id):
        try:
            return Turma.objects.get(id=id)
        except:
            return None