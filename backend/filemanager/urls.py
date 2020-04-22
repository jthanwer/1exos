from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ExerciceViewSet, CorrectionViewSet

router = DefaultRouter()
router.register(r'exercices', ExerciceViewSet, base_name='exercices')
router.register(r'corrections', CorrectionViewSet, base_name='corrections')

urlpatterns = [
    path('', include(router.urls))
]