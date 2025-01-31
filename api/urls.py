#API/URLS.PY
from rest_framework import routers
from django.urls import path
from .views import PostViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post_api')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 📌 Obtener token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 📌 Refrescar token
] + router.urls
