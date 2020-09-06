from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import *
from accounts.models import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from django.conf import settings

from accounts.utils import (get_tokens_for_user,check_invitaion_validity,send_mail_to_invite,
mutual_friend_list,friendhip_status)

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
from django.db.models import Q

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
                connection_object1 = Connection.objects.create(from_user=sender,to_user=user)
                connection_object2 = Connection.objects.create(from_user=user,to_user=sender)

           
            if user:               
                token = get_tokens_for_user(user=user)
                json_data = serializer.data

                json_data['user_id'] = user.id
                json_data['user_profile_id'] = user_profile.id
                json_data['access'] = token['access']
                json_data['refresh'] = token['refresh']
                return Response({"success":True,'data':json_data,"msg":None}, status=status.HTTP_201_CREATED)

        return Response({"error":(serializer.errors),"success":False}, status=status.HTTP_400_BAD_REQUEST)


class GetProfileInfo(APIView):
    def get(self,request):
        user = request.user
        user_profile = user.userprofile
        

        profile_photo = user_profile.profile_photo.url
        cover_photo = user_profile.cover_photo.url
        dob = user_profile.dob

        
        full_name = str(user.first_name)+" " +str(user.last_name)

        to_send = {
            "profile_photo":profile_photo,
            "full_name":full_name,
            "cover_photo":cover_photo,
            "dob":dob
        }
        return Response({"success":True,"data":to_send,"msg":"ok"},status=200)


class GetOtherProfileInfo(APIView):
    def post(self,request):

        data = request.data
        user_id = data.get('user_id',None)

        if user_id is None:
            return Response({"success":False,"error":{"message":"user_id not present"}},status=404)


        try:
            other_user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"success":False,"error":{"message":"user not found"}},status=404)
            
        user_profile = user.userprofile
        

        profile_photo = user_profile.profile_photo.url
        cover_photo = user_profile.cover_photo.url
        dob = user_profile.dob
        
        
        full_name = str(user.first_name)+" " +str(user.last_name)

        to_send = {
            "profile_photo":profile_photo,
            "full_name":full_name,
            "cover_photo":cover_photo,
            "dob":dob
        }


        return Response({"success":True,"data":{'people':peopl},"msg":"ok"},status=200)





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




class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 5

class GetReceivedFriendRequestList(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, format=None):
        user = request.user
        request_list = FriendshipRequest.objects.filter(to_user=user,rejected__isnull=True)

        new_queryset = request_list.order_by('-created')
        page = self.paginate_queryset(new_queryset)
        to_send = []

        for obj in page:
            thumbnail = obj.from_user.userprofile.profile_photo.url

            full_name = str(obj.from_user.first_name)+" " +str(obj.from_user.last_name)

            mutual_connections_list = mutual_friend_list(user,obj.from_user)
            mutual_connections = len(mutual_connections_list)
            user_id = obj.from_user.id
            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "mutual_connections":mutual_connections,
                "user_id":user_id,
                "request_id":obj.id,


            }
            to_send.append(to_add)
        print("to_send is ",to_send)
        to_send = self.get_paginated_response(to_send)
        print("to_send is ",to_send)
        return Response(to_send.data,status=200)


class GetMutualConnectionList(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    def post(self, request, format=None):
        user = request.user
        data = request.data
        
        user_id = data.get('user_id')
        try:
            other_user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"msg":"user not found"},status=404)

        mutual_connections_list = mutual_friend_list(user,other_user)
        # page = self.paginate_queryset(new_queryset)
        page = self.paginate_queryset(mutual_connections_list)
        to_send = []


        # to_send = []
        # # for obj in page:
        # #     thumbnail = obj.to_user.userprofile.thumbnail.url

        # #     full_name = str(obj.to_user.first_name)+" " +str(obj.to_user.last_name)

        # #     mutual_connections_list = mutual_friend_list(user,obj.to_user)
        # #     mutual_connections = len(mutual_connections_list)
        # #     to_add = {
        # #         "thumbnail":thumbnail,
        # #         "full_name":full_name,
        # #         "mutual_connections":mutual_connections,


        # #     }
        # #     to_send.append(to_add)
        # # print("to_send is ",to_send)
        # # to_send = self.get_paginated_response(to_send)
        # # print("to_send is ",to_send)
        # # return Response(to_send.data,status=200)
        print("page is",page)
        for user_id in page:
            user = User.objects.get(id=user_id)

            thumbnail = user.userprofile.profile_photo.url
            
            full_name = str(user.first_name)+" " +str(user.last_name)
            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "user_id":user_id,
                
            }

            to_send.append(to_add)


        print("to_send is",to_send)
        to_send = self.get_paginated_response(to_send)
        print("to_send is",to_send)
        return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)
      

def deleteconnection(request):

    connection_list = Connection.objects.all()
    for connection in connection_list:
        connection.delete()
    return HttpResponse("deleted")


class GetAllFriendsList(APIView,PaginationHandlerMixin):
    page_size = 1
    
    pagination_class = BasicPagination
    
    def get(self, request, format=None):
        user = request.user
        
        
        sort_type = request.query_params.get('sort_type',None)
        search = request.query_params.get('search',None)
    

        
        new_queryset =  Connection.objects.filter(from_user=user)
        
        if search is not None:

            if ' ' in search:
                first_name_query = ((search.split(" "))[0]).strip()
                last_name_query = ((search.split(" "))[1]).strip()
            else:
                first_name_query = search
                last_name_query = search
            print("search_query is",search)
            print("first_name_query is",first_name_query)
            print("last_name_query is",last_name_query)
            new_queryset = new_queryset.filter(            
                Q(to_user__first_name__icontains=first_name_query) | Q(to_user__last_name__icontains=last_name_query)
                |  Q(to_user__username__icontains=first_name_query) |  Q(to_user__username__icontains=last_name_query)   )
            new_queryset = new_queryset.exclude(id=user.id).distinct()    

            # print("search is",search)
            # qs1 = new_queryset.filter(to_user__first_name__icontains=search)
            # print("qs 1 is",qs1)
            # qs2 = new_queryset.filter(to_user__last_name__icontains=search)
            # print("qs 2 is",qs2)
            # new_queryset = qs1 | qs2


        if sort_type is not None:
            if sort_type=="recently_added":
                new_queryset = new_queryset.order_by('-created_at')
            if sort_type=="first_name":
                new_queryset = new_queryset.order_by('to_user__first_name')

        else:
            new_queryset = new_queryset.order_by('-created_at')
        page = self.paginate_queryset(new_queryset)
        to_send = []
        for obj in page:
            thumbnail = obj.to_user.userprofile.profile_photo.url

            full_name = str(obj.to_user.first_name)+" " +str(obj.to_user.last_name)

            mutual_connections_list = mutual_friend_list(user,obj.to_user)
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
        
        return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)


class HandleFriendRequest(APIView):

    def post(self, request, format=None):
        user = request.user
        data = request.data
        request_id = data.get("request_id")
        request_answer = data.get("request_answer")

        try:
            friendship_request_object = FriendshipRequest.objects.get(id=request_id)
            if friendship_request_object.rejected is not None:
                return Response({"success":False,"error":{"message":"Already Rejected"}},status=403)

        except Exception as e:
            print("error is ",e)
            return Response({"success":False,"error":{"message":"request not found"}},status=404)
            

        if friendship_request_object.to_user != user:
            return Response({"success":False,"error":{"message":"not authorized"}},status=403)
           

        if request_answer != "rejected" and request_answer != "accepted":
            return Response({"success":False,"error":{"message":"not authorized"}},status=403)
            


        if request_answer == "accepted":
            friendship_request_object.accept()

        if request_answer == "rejected":
            friendship_request_object.reject()

        return Response({"success":True,"data":{},"msg":"ok"},status=200)




class SearchBarResults(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    def get(self, request, format=None):
        user = request.user

        search_query =  request.query_params.get('search',None)
        if ' ' in search_query:
            first_name_query = ((search_query.split(" "))[0]).strip()
            last_name_query = ((search_query.split(" "))[1]).strip()
        else:
            first_name_query = search_query
            last_name_query = search_query
        print("search_query is",search_query)
        print("first_name_query is",first_name_query)
        print("last_name_query is",last_name_query)
        user_list = User.objects.filter(            
            Q(first_name__icontains=first_name_query) | Q(last_name__icontains=last_name_query)
            |  Q(username__icontains=first_name_query) |  Q(username__icontains=last_name_query)   )
        user_list = user_list.exclude(id=user.id).distinct()
        user_list = user_list.order_by('first_name')
        page = self.paginate_queryset(user_list)
        to_send = []
        for obj in page:
            friendhip_status_result = friendhip_status(user,obj)
            thumbnail = obj.userprofile.profile_photo.url

            full_name = str(obj.first_name)+" " +str(obj.last_name)

            mutual_connections_list = mutual_friend_list(user,obj)
            mutual_connections = len(mutual_connections_list)

            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "mutual_connections":mutual_connections,
                "friendship_status":friendhip_status_result,
                "user_id":obj.id

            }

            to_send.append(to_add)

        print("to_send is ",to_send)
        people_search_result = self.get_paginated_response(to_send)
        print("to_send is ",to_send)

        return Response({"success":True,"data":{'people':people_search_result.data},"msg":"ok"},status=200)


class SendFriendRequest(APIView):
    def post(self, request, format=None):
        user = request.user
        data = request.data
        user_id = data.get("user_id")
        

        try:
            to_user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"success":False,"error":{"message":"User not found"}},status=404)

        request_object, created = FriendshipRequest.objects.get_or_create(from_user=user,to_user=to_user)




        return Response({"success":True,"data":{'request_id':request_object.id},"msg":"ok"},status=200)

  



