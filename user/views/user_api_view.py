import environ
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, status
from user.models.user import User
from user.serializers.user_serializer import UserSerializer
from rest_framework.response import Response

from user.utils.user_utility import generate_auth_tokens

env = environ.Env()
environ.Env.read_env()
DEFAULT_PASSWORD = env('DEFAULT_PASSWORD')


class UserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('user').get('email')
        password = request.data.get('user').get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password, user.password):
            return Response({'message': 'Invalid email or password!'}, status=status.HTTP_400_BAD_REQUEST)
        data = generate_auth_tokens(user)
        return Response(data, status=status.HTTP_200_OK)


class UserGoogleLoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        access_token = request.data.get('access_token')
        response = requests.get(
            f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={access_token}')
        if response.status_code != 200:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        user_data = response.json()
        email = user_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            first_name, last_name = user_data['name'].split(' ')
            user = User.objects.create_user(
                email=email, password=DEFAULT_PASSWORD, first_name=first_name, last_name=last_name)
        data = generate_auth_tokens(user)
        return Response(data, status=status.HTTP_200_OK)


class UserAccountView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UserLogoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
