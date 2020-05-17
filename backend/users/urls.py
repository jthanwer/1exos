from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path, include, re_path
import django.contrib.auth.views as auth_views

from .viewsets import UserViewSet
from .views import PasswordResetView, PasswordResetConfirmView, activate

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    # -- JWT Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # -- Router
    path('', include(router.urls)),

    # -- Password reset
    path('accounts/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # -- Activate account
    path('accounts/activate/<uidb64>/<token>/', activate, name='activate'),

]