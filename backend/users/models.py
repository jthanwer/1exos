from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # category = models.CharField(max_length=2)
    moneybox = models.DecimalField(max_digits=5, decimal_places=2, default=3, blank=True)

