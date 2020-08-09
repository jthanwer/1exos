from django.contrib import admin
from .models import Exercice, Correction

@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('posteur', 'prix', 'niveau')
    list_filter = ()

@admin.register(Correction)
class CorrectionAdmin(admin.ModelAdmin):
    list_display = ('correcteur', 'enonce', 'prix')
    list_filter = ()

