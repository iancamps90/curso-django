# blog/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

def post_list(request):
    post_list = Post.objects.filter(published=True)
    paginator = Paginator(post_list, 5)  # Muestra 5 posts por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'post/list.html', {'page_obj': page_obj})

    
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Se agregó el comentario con éxito")
    else:
        comment_form = CommentForm()
    
    return render(request, 'post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })



@login_required
def create_post(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Se creo el post con éxito")
            return render(request, 'post/createpost.html', {'new_post': post})

    else:
        form = PostForm()
    
    return render (request, 'post/createpost.html', {'form':form})
