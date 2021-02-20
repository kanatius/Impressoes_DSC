from .repository import UsuarioRepository



class UsuarioService:

    def __init__(self):
        super().__init__()
        self.usuarioRepository = UsuarioRepository()

    def getUserName(self, request, id):
        usuario = self.usuarioRepository.getById(id)

        if usuario is not None:
            return usuario.getFullName()
    
        return None 


