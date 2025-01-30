# blog/forms.py
from django import forms
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Titulo para el post', max_length=250)
    body = forms.CharField(label='Contenido', widget=forms.Textarea)
    published = forms.BooleanField(label="¿Publicar?")
    
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'published', 'author', 'categories']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')