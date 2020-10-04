from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from notifications.models import Notification

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'niveau', 'option', 'voie',
              'tirelire', 'is_active', 'is_new',
              'prefix_prof', 'nom_prof', 'ville_etablissement', 'nom_etablissement')
    list_display = ('username', 'id', 'email', 'niveau', 'tirelire')
    list_filter = ()



