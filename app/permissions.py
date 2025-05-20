from rest_framework.permissions import BasePermission

# Definição das permissões da api

# Só permite que determinada pessoa tenha acesso aquela função se ela estiver cadastrada como gestor no banco de dados 
class IsGestor(BasePermission):
    message = "Apenas pessoas cadastradas como Gestor podem ter acesso a essa funcionalidade"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo =='G'

# Permite que pessoas cadastradas como professor tenham acesso a determinada função   
class IsProfessor (BasePermission):
    # permissão para acessar um método (view...)
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'P'
    

# Só permite que determinada pessoa tenha acesso aquela função se ela estiver cadastrada como gestor ou dono no banco de dados
class IsDonoOuGestor(BasePermission):
    # permissão para consultar um objeto específico
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.tipo == 'G':
            return True
        return obj.professor == request.user