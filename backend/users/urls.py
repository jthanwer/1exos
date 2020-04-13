from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    path('', include(router.urls))
]