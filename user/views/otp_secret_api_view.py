
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, status
from user.models.user import User
from user.serializers.user_serializer import UserSerializer
from rest_framework.response import Response
import pyotp
from datetime import datetime

class OTPSecretCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        secret = pyotp.random_base32()
        otp_url = pyotp.totp.TOTP(secret).provisioning_uri(name=request.user.email, issuer_name='Sphere AI')
        user = User.objects.get(id=request.user.id)

        if not user.otp_secret:
            user.otp_secret = secret
            user.save()
        return Response({'qr_link': otp_url})

class OTPSecretVerifyView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        totp = pyotp.TOTP(user.otp_secret)
        is_verfied = totp.verify(request.data['otp_code'])

        if is_verfied:
            user.otp_verified_at = datetime.now()
            user.is_otp_enabled = True
            user.save()
            return Response({'message':'Successfully verified'})
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
