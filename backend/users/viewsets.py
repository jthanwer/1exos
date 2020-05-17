from rest_framework import generics, status, viewsets, filters
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, action

from core.payment import stripe_validate_payment, stripe_create_payment

from .models import CustomUser
from .permissions import IsAdminOrIsSelf
from .serializers import RegistrationSerializer, UserSerializer, \
    PasswordChangeSerializer, UpdateUserSerializer, PasswordResetSerializer

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        if self.action == 'create':
            return RegistrationSerializer
        elif self.action == 'update':
            return UpdateUserSerializer
        elif self.action == 'reset_password':
            return PasswordResetSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        elif self.action == 'client_secret':
            return PaymentIntentSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'set_password']:
            # permission_classes = [IsAdminOrIsSelf]
            permission_classes = [AllowAny]
        elif self.action == 'list':
            # permission_classes = [IsAdminUser]
            permission_classes = [AllowAny]
        else:
            # permission_classes = [IsAuthenticated]
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            current_site = get_current_site(request)
            mail_subject = 'Active ton compte 1Exo'
            message = render_to_string('registration/acc_active_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'user': user,
                'token': default_token_generator.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response(serializer.data,
                            status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_pw = serializer.validated_data.get('old_password', '')
            if user.check_password(old_pw):
                new_pw = serializer.validated_data['new_password']
                user.set_password(new_pw)
                user.save()
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def my_profile(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def check_credentials(self, request):
        data = request.data
        if 'email' in data:
            email = data['email']
            qs = CustomUser.objects.filter(email=email)
            exists = qs.exists()
        else:
            username = data['username']
            qs = CustomUser.objects.filter(username=username)
            exists = qs.exists()
        is_active = qs[0].is_active if exists else True
        return Response({'unique': not exists,
                         'is_active': is_active},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def stripe_create_payment(self, request):
        return stripe_create_payment(request)

    @action(detail=False, methods=['post'])
    def stripe_validate_payment(self, request):
        return stripe_validate_payment(request)






