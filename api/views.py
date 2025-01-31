# api/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from blog.models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrAdmin  # Importamos el permiso personalizado

class PostViewSet(viewsets.ModelViewSet):
    """
    API para gestionar posts:
    - Usuarios normales solo pueden ver posts publicados.
    - Editores pueden ver todos los posts y modificar/eliminar sus propios posts.
    - Admins pueden hacer todo.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdmin]

    def get_queryset(self):
        """ 
        - Admins ven todos los posts.
        - Editores ven todos los posts, pero solo pueden modificar los suyos.
        - Usuarios normales solo ven posts publicados.
        """
        user = self.request.user
        if user.is_staff or user.groups.filter(name="Admin").exists():
            return Post.objects.all()
        elif user.groups.filter(name="Editor").exists():
            return Post.objects.all()
        return Post.objects.filter(published=True)

    def perform_create(self, serializer):
        """ Asignar el usuario autenticado como autor del post """
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """ 
        Solo el autor o un admin pueden eliminar un post.
        """
        instance = self.get_object()
        
        if instance.author != request.user and not request.user.is_staff:
            return Response({"detail": "No tienes permiso para eliminar este post."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"detail": "Post eliminado con éxito."}, status=status.HTTP_204_NO_CONTENT)
