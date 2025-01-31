# blog/admin.py
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Category

#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published']
    list_filter = ['published']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Comment)
admin.site.register(Category)


# Crear grupos automáticamente
def create_groups():
    editor_group, created = Group.objects.get_or_create(name="Editor")
    user_group, created = Group.objects.get_or_create(name="Usuario")

    post_content_type = ContentType.objects.get_for_model(Post)

    editor_permissions = Permission.objects.filter(content_type=post_content_type)
    editor_group.permissions.set(editor_permissions)

    print("✅ Grupos creados correctamente")

create_groups()