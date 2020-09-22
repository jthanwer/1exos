from django.contrib import admin
from .models import Exercice, Correction

@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('id', 'posteur', 'prix', 'niveau')
    fields = ('posteur', 'prix', 'file', 'niveau', 'option',
              'ville_etablissement', 'nom_etablissement', 'prefix_prof', 'nom_prof',
              'type', 'devoir', 'chapitre', 'livre', 'num_page', 'num_exo', 'date_limite')
    list_filter = ()

@admin.register(Correction)
class CorrectionAdmin(admin.ModelAdmin):
    fields = ('correcteur', 'enonce', 'file', 'prix', 'gain', 'is_favorite')
    list_display = ('id', 'correcteur', 'enonce', 'prix')
    list_filter = ()

