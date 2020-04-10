from django.db import models
from django.conf import settings
from users.models import CustomUser
from django.utils import timezone


class Exercice(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,
    #                          related_name='exercices')
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(null=True, max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.name)
