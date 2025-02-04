# blog/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Category
from django.core.exceptions import ValidationError
from django.utils.text import slugify



# FORMULARIO REGISTRO USUARIO
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu contraseña'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite tu contraseña'}),
        label="Confirmar contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def clean_password2(self):
        """ Verifica que las contraseñas coincidan """
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    

# FORM AÑADIR POST
class PostForm(forms.ModelForm):
    """ Formulario para crear y editar posts con validaciones personalizadas """
    title = forms.CharField(
        label='Título del post',
        max_length=250,
        min_length=5,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Agregar Bootstrap
            'placeholder': 'Introduce un título válido'
        })
    )

    body = forms.CharField(
        label='Contenido',
        required=True,
        min_length=20,
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Agregar Bootstrap
            'placeholder': 'Escribe el contenido aquí...',
            'rows': 5
        })
    )
    
    published = forms.BooleanField(
        label="¿Publicar?",
        required=False,  # Evita errores si el usuario lo deja vacío
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'published', 'categories']
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        
        
    def clean_title(self):
        """ Validar que el título no contenga caracteres prohibidos """
        title = self.cleaned_data.get('title')
        if '<' in title or '>' in title or '"' in title:
            raise ValidationError("El título no puede contener caracteres especiales como < > \" ")
        return title
    
    # El slug se genera automáticamente si no se introduce uno.Se evita duplicidad de slugs.  
    def clean_slug(self):
        """Validar que el slug sea único y corregirlo si es necesario."""
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title'))
        if Post.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Este slug ya está en uso. Por favor, elige otro.")
        return slug
        
        
    def save(self, commit=True, user=None):
        """Asignar el autor automáticamente."""
        post = super().save(commit=False)
        if user:
            post.author = user  # Asigna el usuario autenticado como autor
        if commit:
            post.save()
            self.save_m2m()
        return post
    
    
# FORM COMENTARIOS    
class CommentForm(forms.ModelForm):
    """ Formulario para los comentarios con validaciones de seguridad """
    body = forms.CharField(
        label="Comentario",
        min_length=5,
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Escribe tu comentario...', 'rows': 3}),
        error_messages={'min_length': "El comentario debe tener al menos 5 caracteres."}
    )

    class Meta:
        model = Comment
        fields = ['body']
        
        
    def clean_body(self):
        """ Evitar que se inserten caracteres maliciosos en los comentarios """
        body = self.cleaned_data.get('body')
        if '<script>' in body.lower():
            raise ValidationError("¡No intentes inyectar código en los comentarios!")
        return body


    def save(self, commit=True, user=None, post=None):
        """Asigna el usuario y post automáticamente."""
        comment = super().save(commit=False)
        if user:
            comment.author = user.username  # Guarda el nombre de usuario
        if post:
            comment.post = post
        if commit:
            comment.save()
        return comment
