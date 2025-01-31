#  blog/urls.py
from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView


app_name = 'blog'

urlpatterns = [
        path('', views.post_list, name='post_list'),
        path('<int:id>/', views.post_detail, name='post_detail'),
        path('create-post/', views.create_post, name='create_post'),
        path('edit/<int:pk>/', PostUpdateView.as_view(), name='edit_post'),
        path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
    ]