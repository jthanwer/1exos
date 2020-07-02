from django.db import models
from django.conf import settings
from django.utils import timezone


class Exercice(models.Model):
    posteur = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='posted_exos')
    niveau = models.IntegerField()
    prefix_prof = models.BooleanField(default=True)
    nom_prof = models.CharField(max_length=100, default="Admin")
    ville_etablissement = models.CharField(max_length=40, default="Admin")
    nom_etablissement = models.CharField(max_length=100, default="Admin")
    chapitre = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    file = models.FileField(null=True, blank=True, max_length=100)
    livre = models.CharField(null=True, blank=True, max_length=100)
    num_page = models.IntegerField(null=True, blank=True)
    num_exo = models.IntegerField(null=True, blank=True)
    prix = models.IntegerField(default=1)
    date_limite = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.name)


class Correction(models.Model):
    correcteur = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='posted_correcs')
    enonce = models.ForeignKey(Exercice,
                               on_delete=models.CASCADE,
                               related_name='correcs')
    file = models.FileField(null=True, max_length=255)
    prix = models.IntegerField(default=1)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.name)
