from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ExerciceViewSet, CorrectionViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'exercices', ExerciceViewSet, base_name='exercices')
router.register(r'corrections', CorrectionViewSet, base_name='corrections')
router.register(r'ratings', RatingViewSet, base_name='ratings')

urlpatterns = [
    path('', include(router.urls))
]