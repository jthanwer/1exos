from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from .models import Exercice, Correction, Rating

import core.fluxes as fluxes
import core.files as files

@receiver(pre_delete, sender=Exercice)
def delete_file_exercice(sender, instance, **kwargs):
    instance.file.delete(save=True)

@receiver(pre_delete, sender=Correction)
def delete_file_correction(sender, instance, **kwargs):
    fluxes.delete_correction(instance)
    instance.file.delete(save=True)

@receiver(post_save, sender=Rating)
@receiver(post_save, sender=Rating)
def save_rating(sender, instance, **kwargs):
    # -- Si le posteur de l'exo met une note inférieure à 4,
    # on supprime la correction et on fait des transferts de points
    voter = instance.voter
    if voter == instance.correc.enonce.posteur and instance.value < 4:
        instance.correc.delete()

