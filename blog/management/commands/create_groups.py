from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post

class Command(BaseCommand):
    help = 'Crea grupos de usuario y asigna permisos'

    def handle(self, *args, **kwargs):
        # Crear grupo de editores
        editor_group, created = Group.objects.get_or_create(name='Editor')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Editor" creado'))
        
        # Crear grupo de usuarios normales
        user_group, created = Group.objects.get_or_create(name='Usuario')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Usuario" creado'))

        # Obtener permisos para editar pero no eliminar posts
        content_type = ContentType.objects.get_for_model(Post)
        permissions = Permission.objects.filter(content_type=content_type)

        for perm in permissions:
            if perm.codename in ['add_post', 'change_post']:  # Solo agregar y editar
                editor_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Permisos asignados a "Editor"'))
