from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from filemanager.models import Correction
import core.constants as cst


class CustomUser(AbstractUser):
    tirelire = models.IntegerField(default=cst.START_POINTS, blank=True)
    classe = models.IntegerField(default=0)
    sexe_prof = models.BooleanField(default=True)
    nom_prof = models.CharField(max_length=100, default="Admin")
    etablissement = models.CharField(max_length=100, default="Admin")
    correc = models.ManyToManyField(Correction, related_name='buyers')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
