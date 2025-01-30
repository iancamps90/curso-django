
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from blog.models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination  # Añade esta línea para especificar la clase de paginación
