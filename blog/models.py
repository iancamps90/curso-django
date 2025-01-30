# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, db_index=True)  # Añadir índice para mejorar rendimiento
    body = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False) # Autor del post
    categories = models.ManyToManyField('Category', related_name='posts')  # Relación muchos a muchos con Category

    def __str__ (self):
        return self.title
    

#Sistema de Comentarios
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


# Sistema de Categorías
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nombre de la categoría
    description = models.TextField(blank=True, null=True)  # Descripción opcional de la categoría

    def __str__(self):
        return self.name
