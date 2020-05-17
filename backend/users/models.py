from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from filemanager.models import Correction


class CustomUser(AbstractUser):
    tirelire = models.DecimalField(max_digits=5, decimal_places=2, default=3, blank=True)
    classe = models.IntegerField(default=0)
    sexe_prof = models.BooleanField(default=True)
    nom_prof = models.CharField(max_length=100, default="Admin")
    etablissement = models.CharField(max_length=100, default="Admin")
    correc = models.ManyToManyField(Correction, related_name='buyers')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
