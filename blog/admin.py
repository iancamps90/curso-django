# blog/admin.py
from django.contrib import admin
from .models import Post, Comment, Category

#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'body', 'published']
    list_filter = ['published']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Comment)
admin.site.register(Category)
