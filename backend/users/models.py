from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    category = models.CharField(max_length=2)

