from django.db import models
from django.conf import settings
from django.utils import timezone


class Exercice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='exercices')
    classe = models.IntegerField()
    category = models.CharField(max_length=100)
    file = models.FileField(null=True, blank=True, max_length=100)
    manuel = models.CharField(null=True, blank=True, max_length=100)
    num_page = models.IntegerField(null=True, blank=True)
    num_exo = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.name)


class Correction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='corrections')
    enonce = models.ForeignKey(Exercice,
                               on_delete=models.CASCADE,
                               related_name='corrections')
    file = models.FileField(null=True, max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.name)
