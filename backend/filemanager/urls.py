from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ExerciceViewSet

router = DefaultRouter()
router.register(r'exercices', ExerciceViewSet, base_name='data')

urlpatterns = [
    path('', include(router.urls))
]