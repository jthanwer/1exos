from django.test import TestCase
from users.models import CustomUser
import os

os.system('rm -f ./filemanager/migrations/00*')
os.system('rm -f ./users/migrations/00*')
os.system('python manage.py reset_db')
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

