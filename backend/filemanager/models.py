from django.db import models
from django.conf import settings
from django.utils import timezone
from exos_app.settings.storage_backends import PrivateMediaStorage
import core.files as files
import core.fluxes as fluxes
from notifications.signals import notify


class Exercice(models.Model):
    posteur = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='posted_exos')
    niveau = models.IntegerField()
    option = models.CharField(max_length=100, blank=True, null=True)
    voie = models.CharField(max_length=100, blank=True, null=True)
    prefix_prof = models.BooleanField(default=True)
    nom_prof = models.CharField(max_length=100, default="Admin")
    ville_etablissement = models.CharField(max_length=40, default="Admin")
    nom_etablissement = models.CharField(max_length=100, default="Admin")
    type = models.CharField(max_length=10)
    devoir = models.CharField(max_length=10, blank=True, null=True)
    chapitre = models.CharField(max_length=100)
    file = models.FileField(null=True, blank=True, max_length=100)
    livre = models.CharField(null=True, blank=True, max_length=100)
    num_page = models.IntegerField(null=True, blank=True)
    num_exo = models.IntegerField(null=True, blank=True)
    prix = models.IntegerField(default=1)
    date_limite = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Exercice_{}'.format(self.id)

    def save(self, *args, **kwargs):
        if kwargs.get('force_insert', False):
            file = self.file
            self.file = None
            super(Exercice, self).save(*args, **kwargs)

            if file:
                self.file = files.compress_file(file, self.id)
                super(Exercice, self).save(force_update=True)

        else:
            previous_file = Exercice.objects.get(id=self.id).file

            if previous_file != self.file:
                previous_file.delete(save=False)
                self.file = files.compress_file(self.file, self.id)

            super(Exercice, self).save(force_update=True)


class Correction(models.Model):
    correcteur = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='posted_correcs')
    enonce = models.ForeignKey(Exercice,
                               on_delete=models.CASCADE,
                               related_name='correcs')
    file = models.FileField(null=True, blank=True, max_length=255,
                            storage=PrivateMediaStorage())
    prix = models.IntegerField(default=1)
    gain = models.IntegerField(blank=True, default=1)
    is_favorite = models.BooleanField(blank=True, default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Correction_{}_{}'.format(self.enonce.id, self.id)

    def save(self, *args, **kwargs):
        if kwargs.get('force_insert', False):
            file = self.file
            self.file = None
            super(Correction, self).save(*args, **kwargs)
            self.file = files.compress_file(file, self.id, enonce_id=self.enonce_id)
            super(Correction, self).save(force_update=True)
            posteur = self.enonce.posteur
            if posteur != self.correcteur:
                notify.send(self.correcteur,
                            recipient=posteur,
                            verb='correction_posted',
                            action_object=self,
                            target=self.enonce)

        else:
            previous_file = Correction.objects.get(id=self.id).file

            if previous_file != self.file:
                previous_file.delete(save=False)
                self.file = files.compress_file(self.file, self.id, enonce_id=self.enonce_id)
            super(Correction, self).save(force_update=True)


class Rating(models.Model):
    correc = models.ForeignKey(Correction,
                               on_delete=models.CASCADE,
                               related_name='ratings')
    voter = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='ratings')
    value = models.IntegerField()
