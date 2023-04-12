from rest_framework.decorators import api_view
import pyotp
from rest_framework.response import Response
from rest_framework import status
import datetime

@api_view(['POST'])
def create_otp_secret(request):
    # check if user has an otp_secret, save in database if not
    secret = pyotp.random_base32()
    # add user email as argument below
    opt_url = pyotp.totp.TOTP(secret).provisioning_uri(issuer_name='Sphere AI')
    
    return Response({'qr_link': opt_url})

@api_view(['POST'])
def verify_otp(request, *args, **kwargs):
    # get user secret from database then verify the token
    totp = pyotp.TOTP('HTXNTD6LBK4N4DREWYMRBPVCUGDYHKEA')
    is_verfied = totp.verify(kwargs['otp_code'])

    if is_verfied:
        # save the current date time in database and save is enabled to true
        # user.save()
        return Response({'message':'Successfully verified'})
    else:
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
