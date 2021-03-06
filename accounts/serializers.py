from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# for reseting password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse

# from .models import ShoppingList, Inventory
from .utils import Util
from django.conf import settings




User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'firstname', 'lastname','blood','DOB']
       
    def save_user(self, validated_data):
        user = User.objects.create_user( 
                                password=validated_data.get('password'), 
                                email=validated_data.get('email'),
                                firstname=validated_data.get('firstname'),
                                lastname=validated_data.get('lastname'),
                                blood=validated_data.get('blood'),
                                DOB=validated_data.get('DOB')
                                )
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=666)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=3)
    tokens = serializers.CharField(max_length=68, min_length=8, read_only=True)

    class Meta:
        model=User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):

        email = attrs.get('email','')
        password = attrs.get('password', '')

        filtered_user_by_email = User.objects.filter(email=email)
        auth_user = auth.authenticate(email=email, password=password)

        if not auth_user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not auth_user.is_active:
            raise AuthenticationFailed("Email not verified yet!!")

        tokens = RefreshToken.for_user(user=auth_user)
        return {
            'email': auth_user.email,
            'name': (auth_user.firstname +" "+ auth_user.lastname),
            'refresh': str(tokens),
            'access': str(tokens.access_token)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


# from . import google
# from .register import register_social_user
# import os
# from rest_framework.exceptions import AuthenticationFailed
# from decouple import config

# class GoogleSocialAuthSerializer(serializers.Serializer):
#     auth_token = serializers.CharField()

#     def validate_auth_token(self, auth_token):
#         user_data = google.Google.validate(auth_token)
#         try:
#             user_data['sub']
#         except:
#             raise serializers.ValidationError('The token is invalid or expired. Please login again')
        
#         if user_data['aud'] != config('GOOGLE_CLIENT_ID'):
#             raise AuthenticationFailed('oops, who are you?')
        
#         user_id = user_data['sub']
#         email = user_data['email']
#         first_name = user_data['given_name']
#         last_name = user_data['family_name']
#         provider = 'google'

#         return register_social_user(provider = provider, user_id = user_id, email = email, first_name=first_name,last_name=last_name)
