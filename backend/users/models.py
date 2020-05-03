from django.db import models
from django.contrib.auth.models import AbstractUser
from filemanager.models import Correction


class CustomUser(AbstractUser):
    tirelire = models.DecimalField(max_digits=5, decimal_places=2, default=3, blank=True)
    classe = models.IntegerField()
    prof = models.CharField(max_length=100)
    etablissement = models.CharField(max_length=100)
    correc = models.ManyToManyField(Correction, related_name='buyers')

