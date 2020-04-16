from rest_framework import serializers
from users.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def save(self):
        cleaned_data = {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
        }
        user = CustomUser.objects.create_user(**cleaned_data)
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'email')


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class UpdateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=True)
    email = serializers.EmailField(max_length=254, allow_blank=True)

    def update(self, instance, validated_data):
        username = validated_data.get('username', '')
        email = validated_data.get('email', '')
        self.check_unicity_username(instance, username)
        self.check_unicity_email(instance, email)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def check_unicity_username(self, instance, value):
        if CustomUser.objects.filter(username=value).exists() and not \
                instance.username == value:
            error = 'Ce pseudo est déjà pris par un autre utilisateur'
            raise serializers.ValidationError(error)

    def check_unicity_email(self, instance, value):
        if CustomUser.objects.filter(email=value).exists() and not \
                instance.email == value:
            error = 'Cette adresse e-mail est déjà prise par un autre utilisateur'
            raise serializers.ValidationError(error)


class PaymentIntentSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    currency = serializers.CharField(max_length=3)

    def validate_amount(self, value):
        if value < 0.50:
            error = 'Le montant doit être supérieur à 50cts'
            raise serializers.ValidationError(error)
        return int(value * 100)



