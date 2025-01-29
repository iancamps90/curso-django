from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, db_index=True)  # Añadir índice para mejorar rendimiento
    body = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Autor del post


    def __str__ (self):
        return self.title