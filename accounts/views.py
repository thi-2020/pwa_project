from django.shortcuts import render

# Create your views here.
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from .models import ExampleModel
from django.http import HttpResponse
import datetime

        






# from django.shortcuts import render
# from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import filters
from accounts.serializers import *
from accounts.models import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
# import requests
# import random

# from django.core.mail import send_mail
# from django.conf import settings

# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from django.utils.encoding import force_bytes,force_text
# from django.contrib.sites.shortcuts import get_current_site
# from rest_framework.decorators import api_view,permission_classes
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# class TokenGenerator(PasswordResetTokenGenerator):
#       pass
#     # make_token(),check_token()
# account_activation_token = TokenGenerator() 


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserCreate(APIView):
    permission_classes = [AllowAny,]


    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print("@84")
            data=request.data
            email= data['email']
            password=data['password']
            phone=data['phone']
            first_name=data['first_name']
            last_name=data['last_name']
            print("email is ",email)
            user = Test2User(phone=phone,last_name=last_name,
                        email=email,password=password,first_name=first_name)
            user.save()
            print("94")
            return Response({"msg":"User created"}, status=status.HTTP_201_CREATED)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class index(APIView):

    def get(self, request, *args,**kwrgs):
        print("came here@11")
        # cluster = Cluster(['127.0.0.1'])
        # session = cluster.connect()
        # session.set_keyspace('db1')
        print("request user",request.user)
        time = datetime.datetime.now()
        print("time is",time)
        # insert = ExampleModel(description="testing descritiopn at alpha")
        # insert.save()
        #cluster.shutdown()

        qs = ExampleModel.objects.all()
        print("qs is ",qs)

        print("type of qs is",type(qs))
        for q in qs:
            print("example id is",q.example_id," and description is",q.description)
        print("@18")
        return Response({"success":"dhgxhsgd"}, status=status.HTTP_201_CREATED)