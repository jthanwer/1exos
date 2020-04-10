from django.urls import path, include
from users.views import RegisterView, UserProfileView, ChangePasswordView
from users import views as uv

urlpatterns = [
    path('auth/registration/', RegisterView.as_view()),
    path('user/profile/', UserProfileView.as_view(), name='profile'),
    path('user/profile/change_password/', ChangePasswordView.as_view(), name='change_password'),
]