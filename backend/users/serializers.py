from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings

from .models import CustomUser


class BasicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'niveau', 'is_active',
                  'nom_etablissement', 'ville_etablissement',
                  'nom_prof', 'prefix_prof')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'email',
                  'is_active', 'niveau', 'option',
                  'nom_etablissement', 'ville_etablissement',
                  'nom_prof', 'prefix_prof',
                  'tirelire',
                  'unlocked_correcs', 'posted_correcs',
                  'posted_exos', 'liked_exos')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'niveau', 'option',
                  'nom_etablissement', 'ville_etablissement',
                  'nom_prof', 'prefix_prof')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'is_active', 'option',
                  'niveau', 'nom_etablissement', 'ville_etablissement',
                  'nom_prof', 'prefix_prof')

    def save(self, **kwargs):
        cleaned_data = {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
            'niveau': self.validated_data.get('niveau', ''),
            'option': self.validated_data.get('option', ''),
            'nom_etablissement': self.validated_data.get('nom_etablissement', ''),
            'ville_etablissement': self.validated_data.get('ville_etablissement', ''),
            'prefix_prof': self.validated_data.get('prefix_prof', ''),
            'nom_prof': self.validated_data.get('nom_prof', ''),
        }
        user = CustomUser.objects.create_user(**cleaned_data, **kwargs)
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class PaymentIntentSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    currency = serializers.CharField(max_length=3)

    def validate_amount(self, value):
        if value < 0.50:
            error = 'Le montant doit être supérieur à 50cts'
            raise serializers.ValidationError(error)
        # Convert the given value into cents for Stripe
        return int(value * 100)


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = PasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = CustomUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()



