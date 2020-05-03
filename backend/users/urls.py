from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from .viewsets import UserViewSet
from .views import PasswordResetView, PasswordResetConfirmView

from django.http import HttpResponse
import django.contrib.auth.views as auth_views



def empty_view(request):
    return HttpResponse('')


router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    path('', include(router.urls)),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),

    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]