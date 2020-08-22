from filemanager.models import Exercice
import os

Exercice.objects.all().delete()
os.system('python manage.py sqlsequencereset filemanager | python manage.py dbshell')
