from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import (mixins, generics, status, permissions)
from rest_framework_simplejwt.tokens import RefreshToken
from django.http.response import HttpResponse, JsonResponse
import jwt
from rest_framework.views import APIView
# from drf_spectacular.utils import extend_schema, OpenApiParameter
# from drf_spectacular.types import OpenApiTypes
from rest_framework import (mixins, generics, status, permissions)
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#reseting password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from decouple import config
from django.shortcuts import redirect, render
import os
# Create your views here.

from .utils import Util
from .serializers import UserSerializer, EmailVerificationSerializer, LoginSerializer,LogoutSerializer

User = get_user_model()

class SignUp(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer1 = UserSerializer(data=request.data)
        if serializer1.is_valid():
            user_data = serializer1.save_user(serializer1.data)
            token = RefreshToken.for_user(user_data).access_token
            relative_link = reverse('EmailVerification')
            current_site = get_current_site(request).domain
            abs_url = current_site + relative_link + "?token=" + str(token)
            email_body = "Hiii" + "! Use link below to verify your email \n"+ abs_url
            data ={'email_body': email_body, 'email_subject': "Verify your Email",'to_email':user_data.email}
            Util.send_email(data)
            return JsonResponse({'status': 'created', 'token': str(token)}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Enter token here")

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return JsonResponse({'status': 'Email Successfully Verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return JsonResponse({'error':"Activation Link has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return JsonResponse({'error':"Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'Logged out successfully'},status=status.HTTP_204_NO_CONTENT)



##############SOCIAL AUTH#######################

# class GoogleAuth(generics.GenericAPIView):

#     serializer_class = GoogleSocialAuthSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = ((serializer.validated_data)['auth_token'])
#         return Response(data, status=status.HTTP_200_OK)

# def index(request):
#     GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')
#     content = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID}
#     return render(request, 'index.html', content)
    