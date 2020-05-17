from django.test import TestCase
from users.models import CustomUser
from users.viewsets import *
import os

os.system('rm -f ./filemanager/migrations/00*')
os.system('rm -f ./users/migrations/00*')
os.system('python manage.py reset_db')
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

user1 = CustomUser.objects.create_user(username="cassosdu46",
                                       email="joel.thanwerdas@gmail.com",
                                       password="Zdv:89??",
                                       classe=1,
                                       sexe_prof=0,
                                       nom_prof="Durant",
                                       etablissement="Lycée Clément Marot",
                                       is_active=True)

data_user2 = dict(username="cassosdu45",
                  email="cassosdu45@gmail.com",
                  password="Zdv:89??",
                  classe=1,
                  sexe_prof=0,
                  nom_prof="Durant",
                  etablissement="Lycée Clément Marot",
                  is_active=False)

serializer = RegistrationSerializer(data=data_user2)
if serializer.is_valid():
    user = serializer.save(is_active=False)
    mail_subject = 'Active ton compte 1Exo'
    message = render_to_string('registration/acc_active_email.html', {
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'user': user,
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
