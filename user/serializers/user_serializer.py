from rest_framework import serializers
from user.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_otp_enabled',
                  'password', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True}}
