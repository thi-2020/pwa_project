from django.shortcuts import render

# Create your views here.
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from .models import ExampleModel
from django.http import HttpResponse
import datetime

        

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet




# from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import filters
from accounts.serializers import *
from accounts.models import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
import threading
# import random

from django.core.mail import send_mail
# from django.conf import settings

# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from django.utils.encoding import force_bytes,force_text
# from django.contrib.sites.shortcuts import get_current_site
# from rest_framework.decorators import api_view,permission_classes
from django.template.loader import render_to_string
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
            username = data['username']
            password=data['password']
            phone=data['phone']
            first_name=data['first_name']
            last_name=data['last_name']
            dob=data['dob']
            print("dob in line 73 is",dob)
            print("email is ",email)
            user = User(phone=phone,last_name=last_name,
                        email=email,first_name=first_name,dob=dob,username=username)
            user.set_password(password)
            user.save()
            # invitation_obj = serializer.invitation_obj
            # invitation_obj.accepted = True
            # invitation_obj.save()
            to_send = dict()            
            token = get_tokens_for_user(user=user)

            to_send['user_id'] = user.id
            to_send['first_name'] = user.first_name
            to_send['last_name'] = user.last_name
            to_send['email'] = user.email
            to_send['phone'] = user.phone
            to_send['dob'] = str(user.dob)
            to_send['access'] = token['access']
            to_send['username'] = user['username']

            print("94")
            return Response(to_send, status=status.HTTP_201_CREATED)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



from cassandra.cqlengine.management import  sync_table

class index(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, *args,**kwrgs):
        print("came here@11")
        # cluster = Cluster(['127.0.0.1'])
        # session = cluster.connect()
        # session.set_keyspace('db1')
        print("request user",request.user)
        time = datetime.datetime.now()
        print("time is",time)
        insert = ExampleModel(description="testing descritiopn at alpha")
        insert.save()
        print("insert is ",insert)
        print("insert created at is  ",insert.created_at)
        #cluster.shutdown()
        sync_table(Test2User)
        qs = ExampleModel.objects.all()
        print("qs is ",qs)

        print("type of qs is",type(qs))
        for q in qs:
            print("example id is",q.example_id," and description is",q.description)
        print("@18")
        return Response({"success":"dhgxhsgd"}, status=status.HTTP_201_CREATED)


class SendInvitation(APIView):
    def post(self, request, format='json'):
        serializer = InvitationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            print("@84")
            sender = request.user
            data=request.data

            email= data['email']
            key =  get_random_string(64).lower()
            print("key is ",key)
            invitation_obj = Invitation(sender_id=sender.id,email=email,key=key)
            invitation_obj.save()
            thread = threading.Thread(target=send_mail_to_invite, args=(sender,email,key))
            thread.start()

            return Response({"message":"Invitation sent"}, status=status.HTTP_201_CREATED)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CheckInvitation(APIView):
    permission_classes = [AllowAny,]
    def post(self, request, format='json'):
        data=request.data
        key = data['key']       
        try:
            invitation_obj = Invitation.objects.get(key = key)
        except Exception as e:
            print("error is ",e)
            return Response({"error":"Invalid Link"}, status=status.HTTP_400_BAD_REQUEST)
        if invitation_obj.accepted is True:
            return Response({"error":"Already registered using this email id"}, status=status.HTTP_400_BAD_REQUEST)
        email = invitation_obj.email
    
        return Response({"key":key,'email':email}, status=200)


def send_mail_to_invite(sender,email,key):
    print("sender email is",sender.email)
    print("email is",email)
    print("key is",key)

    context = {
            # ToDo: The URL can (and should) be constructed using pythons built-in `reverse` method.
            'username':sender.username,
            'invite_url': "http://13.235.134.196/signup/?key={key}".format(key=key),
        }
    print("context",context)

    email_html_message = render_to_string('email/invitation.html', context)
    email_plaintext_message = render_to_string('email/invitation.txt', context)
    subject = "Initation to join pwa"
            # to_email = settings.FROM_VERIFICATION_EMAIL_ADDRESS

    msg = EmailMultiAlternatives(
    (subject),
    email_plaintext_message,
    'noreply@qilinlab.com',
    [email]
    )
    msg.attach_alternative(email_html_message, "text/html")

    try:
        msg.send()
        print("sent mail worked thats why came here")
    except Exception as e:
        print("error in sending mail in @284 is",e)

    print("sent")


def create_test_user(request):
    phone = get_random_string(10).lower()
    first_name = get_random_string(10).lower()
    last_name = get_random_string(10).lower()
    username = get_random_string(10).lower()
    password = "Rishabh12@"
    dob = "1995-04-23"
    email = get_random_string(10).lower() + "@gmail.com"
    
    user = User(phone=phone,last_name=last_name,
                        email=email,first_name=first_name,dob=dob,username=username)
    user.set_password(password)
    user.save()
    return HttpResponse("email is {email} password is {password}".format(email=email,password=password))