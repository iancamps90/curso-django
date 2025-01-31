import os
import django
import sys

# 🔹 CONFIGURAR MANUALMENTE `mysite.settings`
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # Subir dos niveles
sys.path.append(BASE_DIR)  # Añadir la ruta base del proyecto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # Asegurar que se carga `settings.py`

# 🔹 INICIALIZAR DJANGO
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment, Category
from faker import Faker
import random
from django.utils.text import slugify

fake = Faker('es_ES')

def create_fake_users(n=10):
    users = []
    for _ in range(n):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="testpassword"
        )
        users.append(user)
    return users

def create_fake_categories(n=5):
    categories = []
    for _ in range(n):
        category = Category.objects.create(name=fake.word())
        categories.append(category)
    return categories

def create_fake_posts(users, categories, n=20):
    for _ in range(n):
        title = fake.sentence(nb_words=6, unique=True)  # Títulos únicos

        slug = slugify(title)  # Generar slug a partir del título

        # Asegurar que no haya duplicados
        while Post.objects.filter(slug=slug).exists():
            slug = f"{slug}-{random.randint(1000, 9999)}"

        post = Post.objects.create(
            title=title,
            slug=slug,  # Agregar el slug único
            body=fake.paragraph(),
            author=random.choice(users),
            published=True
        )
        post.categories.add(random.choice(categories))
        create_fake_comments(post)

def create_fake_comments(post, n=5):
    for _ in range(n):
        Comment.objects.create(
            post=post,
            author=fake.name(),
            body=fake.text(),
            active=True
        )

if __name__ == '__main__':
    print("🔄 Creando datos de prueba...")
    users = create_fake_users()
    categories = create_fake_categories()
    create_fake_posts(users, categories)
    print("✅ ¡Datos de prueba generados exitosamente!")
