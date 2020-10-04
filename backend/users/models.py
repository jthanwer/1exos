from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
import core.constants as cst


class CustomUser(AbstractUser):
    email = models.EmailField('email', max_length=150, unique=True,
                              error_messages={
                                  'unique': _("A user with that email already exists.")
                              })
    is_new = models.BooleanField(default=True)
    tirelire = models.IntegerField(default=cst.START_POINTS, blank=True)
    niveau = models.IntegerField(default=0)
    option = models.CharField(max_length=100, blank=True, null=True)
    voie = models.CharField(max_length=100, blank=True, null=True)
    prefix_prof = models.BooleanField(default=True)
    nom_prof = models.CharField(max_length=100, default="Admin")
    ville_etablissement = models.CharField(max_length=40, default="Admin")
    nom_etablissement = models.CharField(max_length=100, default="Admin")
    unlocked_correcs = models.ManyToManyField('filemanager.Correction', related_name='buyers')
    liked_exos = models.ManyToManyField('filemanager.Exercice', related_name='liked_by')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
