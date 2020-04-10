from django.urls import path, include
from rest_framework.routers import DefaultRouter

from filemanager import views as fmv
from filemanager import viewsets as fmvs

router = DefaultRouter()
router.register(r'files', fmvs.ExerciceViewSet, base_name='data')

urlpatterns = [
    path('', include(router.urls))
]