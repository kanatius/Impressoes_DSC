from .models import Impressao, TipoImpressao, Turma
from django.db.models import Q
#IMPRESSÃO REPOSITORY

class ImpressaoRepository:

    
    def list(self, imprimida=None, cliente_id=None, order_by='id', limit=0, offset=0, imprimida_min_date = None, imprimida_max_date = None, turma_id = None, desc=False, no_tipo = []):
        query = Impressao.objects.all()

        if imprimida is not None:
            query = query.filter(imprimida=imprimida)

        if cliente_id is not None:
            query = query.filter(cliente_id=cliente_id)

        if imprimida_min_date is not None:
            query = query.filter(set_imprimida_em__gte = imprimida_min_date)
        
        if imprimida_max_date is not None:
            query = query.filter(set_imprimida_em__lte = imprimida_max_date)

        if turma_id is not None:
            query = query.filter(turma__id = turma_id)
        
        query = query.order_by(order_by)

        if limit == 0:
            limit = len(query)

        for tipo in no_tipo:
            query = query.filter(~Q(tipo=tipo)) #remove Provas

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
    
    def getAll(self):
        return Turma.objects.all()