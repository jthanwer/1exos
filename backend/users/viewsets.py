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
        elif self.action in ['update', 'partial_update']:
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
            permission_classes = [IsAdminOrIsSelf]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action in ['create', 'check_credentials', 'etablissements', 'profs']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()
        password = request.data.pop('password', '')
        for key in request.data:
            if key in ['username', 'email']:
                if not user.check_password(password):
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def change_password(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_pw = serializer.validated_data.get('old_password', '')
        if not user.check_password(old_pw):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        new_pw = serializer.validated_data['new_password']
        user.set_password(new_pw)
        user.save()
        return Response(status=status.HTTP_205_RESET_CONTENT)

    @action(detail=False)
    def my_profile(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False)
    def set_is_new(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user.is_new = False
        user.save()
        return Response(status=status.HTTP_200_OK)

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
        is_active = qs[0].is_active if exists else False
        return Response({'unique': not exists,
                         'is_active': is_active},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def stripe_create_payment(self, request):
        return stripe_create_payment(request)

    @action(detail=False, methods=['post'])
    def stripe_validate_payment(self, request):
        return stripe_validate_payment(request)

    @action(detail=False)
    def etablissements(self, request):
        queryset = CustomUser.objects.values('ville_etablissement', 'nom_etablissement')\
            .distinct()
        return Response({'results': queryset})

    @action(detail=False)
    def profs(self, request):
        queryset = CustomUser.objects.values('prefix_prof', 'nom_prof', 'ville_etablissement', 'nom_etablissement')\
            .distinct()
        return Response({'results': queryset})








