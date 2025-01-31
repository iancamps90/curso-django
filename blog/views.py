# blog/views.py
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, UserRegistrationForm
from django.views.generic import UpdateView, DeleteView


# 🔹 REGISTRO DE USUARIO
def register_user(request):
    """ Registra un nuevo usuario y le asigna el rol de 'Usuario' """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Obtener o crear el grupo 'Usuario'
            user_group = Group.objects.get(name="Usuario")  
            user.groups.add(user_group)
            
            
            login(request, user)  # Inicia sesión automáticamente 
            messages.success(request, "¡Registro exitoso! Ya puedes crear posts.")
            return redirect('blog:post_list')  # Redirige al listado de posts
    else:
        form = UserRegistrationForm()

    return render(request, 'post/register.html', {'form': form})


# 🔹 LISTA DE POSTS
def post_list(request):
    """Muestra una lista paginada de posts únicos publicados."""
    posts = Post.objects.filter(published=True).distinct().order_by('-created_at')
    paginator = Paginator(posts, 5)  # 5 posts por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'post/list.html', {'page_obj': page_obj})


# 🔹 DETALLE DEL POST + COMENTARIOS  
def post_detail(request, id):
    """ Muestra el detalle de un post junto con los comentarios """
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                messages.success(request, "¡Comentario agregado con éxito!")
                return redirect('blog:post_detail', id=post.id)
        else:
            messages.error(request, "Debes iniciar sesión para comentar.")
            return redirect('login')

    else:
        comment_form = CommentForm()

    return render(request, 'post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


# 🔹 VERIFICAR SI EL USUARIO ES EDITOR O ADMIN
def is_editor_or_admin(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name__in=['Admin', 'Editor']).exists())


# 🔹 CREAR UN POST (Solo Editores o Admins)
@login_required
@user_passes_test(is_editor_or_admin, login_url='blog:post_list', redirect_field_name=None)
def create_post(request):
    """Permite crear un post si el usuario es editor o administrador."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "¡Post creado con éxito!")
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm()

    return render(request, 'post/createpost.html', {'form': form})




# 🔹 EDITAR POST (Solo el autor puede editar)
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/edit_post.html'
    fields = ['title', 'body']

    def get_queryset(self):
        """Solo el autor del post puede editarlo."""
        return Post.objects.filter(author=self.request.user).select_related("author")

    def form_valid(self, form):
        messages.success(self.request, "¡Post editado con éxito!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'id': self.object.id})



# 🔹 ELIMINAR POST (Solo el autor puede eliminar)
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        """ Solo el autor del post puede eliminarlo. """
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "¡Post eliminado con éxito!")
        return super().delete(request, *args, **kwargs)




# 🔹 EDITAR UN POST CON PERMISOS
@login_required
@permission_required('blog.change_post', raise_exception=True)
def edit_post(request, id):
    """ Permite editar un post si el usuario tiene permisos. """
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post actualizado con éxito")
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'post/edit_post.html', {'form': form, 'post': post})
