from .models import Usuario



class UsuarioRepository:

    def __init__(self):
        super().__init__()
    

    def getById(self, id):
        try:
            return Usuario.objects.get(id=id)
        except:
            return None
