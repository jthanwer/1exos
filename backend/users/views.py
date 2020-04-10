from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework import status

from users.models import CustomUser
from users.serializers import CustomUserRegistrationSerializer, CustomUserSerializer


class RegisterView(CreateAPIView):
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(self.request)
            data = {'email': self.request.data['email'],
                    'password': self.request.data['password1']}
            # data_token = TokenObtainPairSerializer().validate(data)
            headers = self.get_success_headers(serializer.data)

            return Response(status=status.HTTP_201_CREATED,
                            headers=headers)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def put(self, request):
        user = request.user
        data = request.data
        old_password = data['old_password']
        new_password = data['new_password']
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        new_data = request.data
        serializer = CustomUserSerializer(request.user)
        user_updated = serializer.update(request.user, new_data)
        serializer_updated = CustomUserSerializer(user_updated)
        return Response(serializer_updated.data)


