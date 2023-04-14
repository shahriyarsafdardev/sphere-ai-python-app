from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers.user_serializer import UserSerializer


def generate_auth_tokens(user):
    refresh = RefreshToken.for_user(user)
    data = {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    }
    return data
