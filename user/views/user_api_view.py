from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, status
from user.models.user import User
from user.serializers.user_serializer import UserSerializer
from rest_framework.response import Response


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
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)

        if not user or not check_password(password, user.password):
            return Response({'error': 'Invalid email or password.'}, status=400)

        refresh = RefreshToken.for_user(user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data
        }
        return Response(data, status=status.HTTP_200_OK)


class UserAccountView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
