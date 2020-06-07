from rest_framework import generics, status, viewsets, filters
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, action

from core.payment import stripe_validate_payment, stripe_create_payment

from users.models import CustomUser
from users.permissions import IsAdminOrIsSelf
from users.serializers import RegistrationSerializer, UserSerializer, \
    PasswordChangeSerializer, UpdateUserSerializer, PasswordResetSerializer

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

user = CustomUser.objects.all()[0]
mail_subject = 'Active ton compte 1Exo'
message = render_to_string('registration/acc_active_email.html', {
    'uid': urlsafe_base64_encode(force_bytes(user.id)),
    'user': user,
    'token': default_token_generator.make_token(user),
})
email = EmailMessage(mail_subject, message, to=[user.email])
email.send()
