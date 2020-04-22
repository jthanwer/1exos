from rest_framework import generics, status, viewsets, filters
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated, \
    IsAdminUser
from rest_framework.decorators import api_view, action

import stripe
import decimal

from .models import CustomUser
from .permissions import IsAdminOrIsSelf
from .serializers import RegistrationSerializer, UserSerializer, \
    PasswordSerializer, UpdateUserSerializer, PaymentIntentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        if self.action == 'create':
            return RegistrationSerializer
        elif self.action == 'update':
            return UpdateUserSerializer
        elif self.action == 'set_password':
            return PasswordSerializer
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
            serializer.save()
            return Response(serializer.data,
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
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
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
    def client_secret(self, request):
        stripe.api_key = 'sk_test_l0DVglzDUUdvrm4xthnZrf5300Lq3X7bez'
        serializer = PaymentIntentSerializer(data=request.data)
        if serializer.is_valid():
            intent = stripe.PaymentIntent.create(**serializer.validated_data)
            return Response(intent)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def validate_payment(self, request):
        stripe.api_key = 'sk_test_l0DVglzDUUdvrm4xthnZrf5300Lq3X7bez'
        user = request.user
        payload = request.data
        payment_intent = stripe.PaymentIntent.retrieve(
            payload['id'],
        )
        if payment_intent.status == "succeeded":
            user.moneybox += decimal.Decimal(payment_intent.amount) / decimal.Decimal(100)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)



