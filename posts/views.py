from django.shortcuts import render,get_object_or_404

# Create your views here.




from .models import *
from .serializers import *
from accounts.serializers import UserDetailSerailizer 
from django.http import HttpResponse

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
# from .permissions import IsOwnerOnly
from django.utils import timezone
from accounts.models import User
import json
from rest_framework.parsers import FormParser, MultiPartParser
from accounts.pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination
from posts.utils import is_feed_post_liked


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 5

class GetPost(APIView):
    def post(self, request):
        requesting_user = request.user

        serializer = PostCreateSerializer(data=request.data)

        if serializer.is_valid():

            post_obj  = serializer.post_obj

            is_liked = is_feed_post_liked(requesting_user,post_obj)            
            image = post_obj.image

            if image.name!=u'':
                print("length of name is ",len(image.name))
                image = image.url
            else:
                image = None    

            if post_obj.is_edited is True:
                timestamp = post_obj.created_at
            else:
                timestamp = post_obj.modified_at

            print("image is",image)            
            to_send = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "user_id":user.id,
                # "activity_message":activity_message,
                "post_id":post_obj.id,
                "is_edited":post_obj.is_edited,
                "is_comment_disabled":post_obj.is_comment_disabled,
                "no_of_likes":post_obj.no_of_likes,
                "no_of_comments":post_obj.no_of_comments,
                "content":post_obj.content,
                "image":image,
                "is_liked":is_liked,
                "timestamp":timestamp,
                "post_type":'Feed',
                
                
            }



            print("to_send is",to_send)

            return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)



class CreatePost(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    def post(self,request):
        
        serializer = PostCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            content = data.get('content',None)
            visibilty_status = data.get('visibilty_status','everyone')
            image = request.data.get('image',None)

            print("image is",image)
            post_obj = FeedPost.objects.create(user=user,content=content,visibilty_status=visibilty_status,
                image = image)
            
            activity_obj = Activity.objects.create(user=user,post_id=post_obj.id,activity_type='create_feed_post')
            

            to_send = {"post_id": post_obj.id}
            return Response({"success":True,"data":to_send,"msg":"post created sucessfully"},status=201)
            
        if serializer.errors:
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}
            
            return Response({"success":False,"error":error},status=400)



class UpdatePost(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    def post(self,request):        
        serializer = PostUpdateOrDeleteSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
  
            data = serializer.data 
            post_obj = serializer.post_obj

            post_obj.visibilty_status = data.get('visibilty_status', post_obj.visibilty_status)
            post_obj.content = data.get('content', post_obj.content)
            post_obj.image = data.get('image', post_obj.image)
            post_obj.save()

            to_send = {"post_id": post_obj.id}
            return Response({"success":True,"data":to_send,"msg":"post updated sucessfully"},status=201)
            
        if serializer.errors:            
            errors = serializer.errors
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}          
            return Response({"success":False,"error":error},status=400)
 


class DeletePost(APIView):

    def post(self,request):
        
        serializer = PostUpdateOrDeleteSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
             
            post_obj = serializer.post_obj

            post_obj.delete()
            activity_obj = Activity.objects.get(user=user,post=post_obj,activity_type='create_post')
            activity_obj.delete()
            to_send = {"post_id": post_obj.id}
            return Response({"success":True,"data":to_send,"msg":"post deleted sucessfully"},status=201)
            
        if serializer.errors:            
            errors = serializer.errors
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}          
            return Response({"success":False,"error":error},status=400)






class SelfTimeline(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    def get(self,request):


        user = request.user
        user_full_name = str(user.first_name)+" " +str(user.last_name)
        full_name = str(user.first_name)+" " +str(user.last_name)
        thumbnail = user.profile_photo.url

        post_list = FeedPost.objects.filter(user=user).order_by('-created_at')
        page = self.paginate_queryset(post_list)
        to_send = []
        print("page is",page)

        for post_obj in page:

            is_liked = is_feed_post_liked(user,post_obj)            
            image = post_obj.image

            if image.name!=u'':
                print("length of name is ",len(image.name))
                image = image.url
            else:
                image = None    



            if post_obj.is_edited is True:
                timestamp = post_obj.created_at
            else:
                timestamp = post_obj.modified_at
            print("image is",image)            
            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "user_id":user.id,
                # "activity_message":activity_message,
                "post_id":post_obj.id,
                "is_edited":post_obj.is_edited,
                "is_comment_disabled":post_obj.is_comment_disabled,
                "no_of_likes":post_obj.no_of_likes,
                "no_of_comments":post_obj.no_of_comments,
                "content":post_obj.content,
                "image":image,
                "is_liked":is_liked,
                "timestamp":timestamp,
                "post_type":'Feed',
                
                
            }

            to_send.append(to_add)


        print("to_send is",to_send)
        to_send = self.get_paginated_response(to_send)
        print("to_send is",to_send)

        return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)

class OthersTimeLine(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    def post(self,request):


        requesting_user = request.user


        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"msg":"user not found"},status=404)

        user_full_name = str(user.first_name)+" " +str(user.last_name)
        full_name = str(user.first_name)+" " +str(user.last_name)
        thumbnail = user.profile_photo.url

        post_list = FeedPost.objects.filter(user=user).order_by('-created_at')
        page = self.paginate_queryset(post_list)
        to_send = []
        print("page is",page)

        for post_obj in page:

            is_liked = is_feed_post_liked(requesting_user,post_obj)            
            image = post_obj.image

            if image.name!=u'':
                print("length of name is ",len(image.name))
                image = image.url
            else:
                image = None    
            if post_obj.is_edited is True:
                timestamp = post_obj.created_at
            else:
                timestamp = post_obj.modified_at
            print("image is",image)            
            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "user_id":user.id,
                # "activity_message":activity_message,
                "post_id":post_obj.id,
                "is_edited":post_obj.is_edited,
                "is_comment_disabled":post_obj.is_comment_disabled,
                "no_of_likes":post_obj.no_of_likes,
                "no_of_comments":post_obj.no_of_comments,
                "content":post_obj.content,
                "image":image,
                "is_liked":is_liked,
                "timestamp":timestamp,
                "post_type":'Feed',
                
                
            }

            to_send.append(to_add)


        print("to_send is",to_send)
        to_send = self.get_paginated_response(to_send)
        print("to_send is",to_send)

        return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)




class NewsFeed(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    def get(self,request):
        requesting_user = request.user
  
        post_list = FeedPost.objects.all().order_by('-created_at')
        page = self.paginate_queryset(post_list)
        to_send = []
        print("page is",page)

        for post_obj in page:
            user = post_obj.user
            is_liked = is_feed_post_liked(requesting_user,post_obj)            
            image = post_obj.image
            full_name = str(user.first_name)+" " +str(user.last_name)
            thumbnail = user.profile_photo.url
            if image.name!=u'':
                print("length of name is ",len(image.name))
                image = image.url
            else:
                image = None    
            if post_obj.is_edited is True:
                timestamp = post_obj.created_at
            else:
                timestamp = post_obj.modified_at
            print("image is",image)            
            to_add = {
                "thumbnail":thumbnail,
                "full_name":full_name,
                "user_id":user.id,
                # "activity_message":activity_message,
                "post_id":post_obj.id,
                "is_edited":post_obj.is_edited,
                "is_comment_disabled":post_obj.is_comment_disabled,
                "no_of_likes":post_obj.no_of_likes,
                "no_of_comments":post_obj.no_of_comments,
                "content":post_obj.content,
                "image":image,
                "is_liked":is_liked,
                "timestamp":timestamp,
                "post_type":'Feed',
                
                
            }

            to_send.append(to_add)


        print("to_send is",to_send)
        to_send = self.get_paginated_response(to_send)
        print("to_send is",to_send)

        return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)



class LikesList(APIView):
    def post(self,request):

        serializer = UserDetailSerailizer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data
            post_obj = serializer.post_obj

 


            
            # posts = FeedPost.objects.filter(user=user,vis)
            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)

class CommentsList(APIView):
    def post(self,request):

        serializer = UserDetailSerailizer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            post_obj = serializer.post_obj            


            
            # posts = FeedPost.objects.filter(user=user,vis)
            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)


class LikePost(APIView):
    def post(self,request):

        serializer = UserDetailSerailizer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            post_obj = serializer.post_obj

            
            # posts = FeedPost.objects.filter(user=user,vis)
            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)

class UnlikePost(APIView):
    def post(self,request):

        serializer = UserDetailSerailizer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            post_obj = serializer.post_obj

            
            # posts = FeedPost.objects.filter(user=user,vis)
            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)


class CreateComment(APIView):
    def post(self,request):

        serializer = UserDetailSerailizer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            
            to_send = {"post_id": post_obj.id}
            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)


class UpdateComment(APIView):
    def post(self,request):

        serializer = UpdateOrDeleteCommentSerailizer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            comment_obj = serializer.comment_obj 
            
            comment_obj.content = data.get('content',comment_obj.content)
            comment_obj.save()

            
            # posts = FeedPost.objects.filter(user=user,vis)
            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)