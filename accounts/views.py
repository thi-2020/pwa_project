from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import *
from accounts.models import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from django.conf import settings

from accounts.utils import (get_tokens_for_user,check_invitaion_validity,send_mail_to_invite)

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.crypto import get_random_string
import threading
# import random
from datetime import timedelta
from django.utils import timezone
from accounts.utils import send_mail
import json

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from .pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination


class TokenGenerator(PasswordResetTokenGenerator):
      pass

account_activation_token = TokenGenerator() 

class UserCreate(APIView):
    permission_classes = [AllowAny,]

    def post(self, request,*args,**kwargs):
        serializer = UserSerializer(data=request.data)
        success = {}
        error = {}
        if serializer.is_valid():
            data=serializer.data
            email= data['email']

            email= data['email']
            username = data['username']
            password=request.data['password']
            phone=data['phone']
            first_name=data['first_name']
            last_name=data['last_name']
            dob=data['dob']

            email = email.lower()


            email = email.replace(" ", "")


            user= User.objects.create_user(email=email,password=password,username=username,
            last_name=last_name,first_name=first_name,phone=phone)
            
            user_profile = UserProfile.objects.create(user=user,dob=dob)

            invitation_obj = serializer.invitation_obj
            invitation_obj.accepted = True
            invitation_obj.save()

            sender = invitation_obj.sender

            if sender.is_staff is False:
                connection_object = Connection.objects.create(sender=sender.userprofile,
                receiver=user.userprofile)

           
            if user:               
                token = get_tokens_for_user(user=user)
                json_data = serializer.data

                json_data['user_id'] = user.id
                json_data['user_profile_id'] = user_profile.id
                json_data['access'] = token['access']
                json_data['refresh'] = token['refresh']
                return Response({"success":True,'data':json_data,"msg":None}, status=status.HTTP_201_CREATED)

        return Response({"error":(serializer.errors),"success":False}, status=status.HTTP_400_BAD_REQUEST)




class SendInvitation(APIView):
    # parser_classes = (JSONParser,FormParser,MultiPartParser)
    def post(self, request,*args,**kwargs):

        sender = request.user
        data = (request.data)
        # data=list(request.data)
        print("request.data is ",request.data)
        # data=json.loads(request.body.decode('utf-8'))
        
        print("request.data is ",data)

        print("count of invitations  is",len(data))
        to_send = []
        for invitation in data:
            
            print("invitation is ",invitation)
            email = invitation.get('email',None)
            phone = invitation.get('phone',None)
            index = invitation['index']


            print("email is",email)
            print("phone is",phone)
            print("index is",index)
            to_add = check_invitaion_validity(sender,email,phone,index)
            # if to_add['is_limit_error'] is True:
            #     to_send.append(to_add)
            #     print("caem in @94")
            #     return Response(to_send, status=200)

            
            if to_add['is_error'] is False:
                key =  get_random_string(64).lower()
                print("key is ",key)

                invitation_obj = Invitation(sender=sender,receiver_email=email,
                invitation_key=key,receiver_phone=phone)
                invitation_obj.save()
    

                thread = threading.Thread(target=send_mail_to_invite, 
                args=(sender,email,key,invitation_obj.id))
                thread.start()



            to_send.append(to_add)

        return Response({"success":True,'data':to_send,"msg":None}, status=200)




class InvitationLeft(APIView):
    def get(self, request, format='json'):


        user = request.user    

        sent_threshold = timezone.now() - timedelta(days = 7)
        print("sent threshold is ",sent_threshold)
        count = Invitation.objects.filter(sender_id = user.id).filter(created_at__gt = sent_threshold).count()        

        invitation_left = 10-count
        to_send = {"invitation_left":invitation_left}
        return Response({"success":True,'data':to_send,"msg":None}, status=200)




class CheckInvitation(APIView):
    permission_classes = [AllowAny,]
    def post(self, request, format='json'):
        data=request.data
        key = data['key']       
        try:
            invitation_obj = Invitation.objects.get(invitation_key = key)
        except Exception as e:
            print("error is ",e)
            return Response({"error":{"message":"Invalid Link"},"sucesss":False}, status=status.HTTP_400_BAD_REQUEST)
        if invitation_obj.accepted is True:
            return Response({"error":{"message":"Already registered using this email id"},"sucesss":False}, status=status.HTTP_400_BAD_REQUEST)
        email = invitation_obj.receiver_email
        phone = invitation_obj.receiver_phone
        to_send = {"key":key,'email':email,'phone':phone} 
        return Response({"success":True,'data':to_send,"msg":None}, status=200)


def testemail(request):

   
    key = "dsdsdsds"
    context = {
            # ToDo: The URL can (and should) be constructed using pythons built-in `reverse` method.
            'username':"mahatma",
            'invite_url': "http://localhost:3000/signup/?key={key}".format(key=key),
        }
    print("context",context)

    html_address = 'email/invitation.html'
    text_address = 'email/invitation.txt'
    subject = "Initation to join pwa"
            # to_email = settings.FROM_VERIFICATION_EMAIL_ADDRESS

    email = "jrishabh89fggfgfgfgfgfg0@gmail.com"
    response = send_mail(email,subject,context,html_address,text_address)
    print("response is",response)
    if response['is_sent'] is False:
        to_add['error']['email'] = "email not sent"
        invitation_obj.delete()


    return HttpResponse("mail sent")

def mutual_friend_list(user1,user2):

    list1 = Connection.objects.filter(sender=user1).values_list('receiver',flat=True) 
    list1 = list(list1)   
    list2 = Connection.objects.filter(receiver = user1).values_list('sender',flat=True)  
    list2 = list(list2)  
    print("type of list 1 is ",type(list1))
    list_a = list1 + list2
    print("lista is",list_a)
    a_set = set(list_a)
    list3 = Connection.objects.filter(sender = user2).values_list('receiver',flat=True) 
    list3 = list(list3)   
    list4 = Connection.objects.filter(receiver = user2).values_list('sender',flat=True)       
    list4 = list(list4)

    list_b = list3 + list4
    b_set = set(list_b)
    result = (a_set.intersection(b_set))
    result_list = list(result) 
    return result_list


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 2

class GetFriendRequestList(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        user = request.user
        request_list = FriendshipRequest.objects.filter(to_user=user)

        new_queryset = request_list.order_by('-created')
        page = self.paginate_queryset(new_queryset)
        to_send = []
        for obj in page:
            thumbnail = obj.from_user.userprofile.thumbnail.url

            full_name = str(obj.from_user.first_name)+" " +str(obj.from_user.last_name)

            mutual_connections_list = mutual_friend_list(user,obj.from_user)
            mutual_connections = len(mutual_connections_list)
            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "mutual_connections":mutual_connections,


            }
            to_send.append(to_add)
        print("to_send is ",to_send)
        to_send = self.get_paginated_response(to_send)
        print("to_send is ",to_send)
        return Response(to_send.data,status=200)


class GetMutualConnectionList(APIView):
    
    def post(self, request, format=None):
        user = request.user
        data = request.data
        
        username = data.get('username')

        other_user = User.objects.get(username=username)

        mutual_connections_list = mutual_friend_list(user,other_user)
        to_send = []

        for user_id in mutual_connections_list:
            user = User.objects.get(id=user_id)

            thumbnail = user.userprofile.thumbnail.url

            full_name = str(user.first_name)+" " +str(user.last_name)
            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                


            }

            to_send.append(to_add)


        print("to_send is",to_send)
        return Response(to_send,status=200)

def deleteconnection(request):

    connection_list = Connection.objects.all()
    for connection in connection_list:
        connection.delete()
    return HttpResponse("deleted")