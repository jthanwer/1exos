from rest_framework import serializers
from users.models import CustomUser


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def validate_email(self, email):
        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                    "Un utilisateur est déjà enregistré avec cette adresse e-mail")
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                "Les deux mots de passes ne sont pas identiques")
        return data

    def save(self, request):
        cleaned_data = {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password1', ''),
        }
        user = CustomUser.objects.create_user(**cleaned_data)
        return user


class CustomUserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username')
