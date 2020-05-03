from django.test import TestCase
from users.models import CustomUser
import os

os.system('rm -f ./filemanager/migrations/00*')
os.system('rm -f ./users/migrations/00*')
os.system('python manage.py reset_db')
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

user1 = CustomUser.objects.create_user(username="cassosdu46", email="joel.thanwerdas@gmail.com",
                                       password="Zdv:89??", classe=1, prof="Mme Durant",
                                       etablissement="Lycée Clément Marot")

user2 = CustomUser.objects.create_user(username="cassosdu45", email="cassosdu45@gmail.com",
                                       password="Zdv:89??", classe=1, prof="Mme Durant",
                                       etablissement="Lycée Clément Marot")
