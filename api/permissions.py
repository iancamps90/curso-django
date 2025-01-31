from rest_framework import permissions

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    - Permite a cualquier usuario ver los posts publicados.
    - Solo el autor del post puede editar o eliminar su propio post.
    - Los administradores pueden editar/eliminar cualquier post.
    """

    def has_permission(self, request, view):
        # Permitir solo lectura para todos los usuarios
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo usuarios autenticados pueden crear posts
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Permitir solo lectura para todos los usuarios
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permitir a los administradores modificar/eliminar cualquier post
        if request.user.is_staff or request.user.groups.filter(name="Admin").exists():
            return True

        # Solo el autor del post puede modificarlo o eliminarlo
        return obj.author == request.user

