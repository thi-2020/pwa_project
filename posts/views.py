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
from posts.utils import is_post_liked,create_activity_and_notification_object


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 5

class GetPost(APIView):
    def post(self, request):
        requesting_user = request.user

        serializer = PostDetailSerializer(data=request.data)

        if serializer.is_valid():

            post_obj  = serializer.post_obj
            user = post_obj.user
            thumbnail = user.profile_photo.url
            is_liked = is_post_liked(requesting_user,post_obj,'Feed')            
            image = post_obj.image
            full_name = str(user.first_name)+" " +str(user.last_name)
            if image.name!=u'':
                print("length of name is ",len(image.name))
                image = image.url
            else:
                image = None    

            if post_obj.is_edited is True:
                timestamp = post_obj.modified_at
            else:
                timestamp = post_obj.created_at

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

            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)
        if serializer.errors:
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}
            
            return Response({"success":False,"error":error},status=400)



class CreatePost(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    def post(self,request):
        
        serializer = PostCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            content = data.get('content',None)
            visibilty_status = data.get('visibilty_status','everyone')
            post_type = data.get('post_type','everyone')
            image = request.data.get('image',None)
        

            print("image is",image)
            post_obj = FeedPost.objects.create(user=user,content=content,visibilty_status=visibilty_status,
                image = image)
            activity_type='create_post'
            feed_post,group_post,activity_obj = create_activity_and_notification_object(
                        user,post_obj,post_type,activity_type)
            

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
            new_content = data.get('content', post_obj.content)
            new_image = data.get('image', post_obj.image)
            print("new_content is",new_content)
            print("new_image is",new_image)

            if new_image==post_obj.image and new_content==post_obj.content:
                is_edited = False
            else:
                is_edited = True
            post_obj.content = new_content
            post_obj.image = new_image
            post_obj.is_edited = is_edited
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
            user = request.user
            post_obj = serializer.post_obj
            post_id = post_obj.id
            print("post_id is",post_id)
            activity_obj_list = Activity.objects.filter(post_id=post_id)
            activity_obj_list.delete()

            post_obj.delete()
            to_send = {"post_id": post_id}
            return Response({"success":True,"data":to_send,"msg":"post deleted sucessfully"},status=201)
            
        if serializer.errors:            
            errors = serializer.errors
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}          
            return Response({"success":False,"error":error},status=400)




class UpdatePostCommentSettings(APIView):
    def post(self,request):
        
        serializer = UpdatePostCommentSettingsSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
            user = request.user
            data = request.data
            post_obj = serializer.post_obj
            is_comment_disabled = post_obj.is_comment_disabled
            comment_status = data['comment_status']

            if comment_status=='disable':
                post_obj.is_comment_disabled = True
                post_obj.save()
            if comment_status=='enable':
                post_obj.is_comment_disabled = False
                post_obj.save()
            
            return Response({"success":True,"data":{},"msg":"updated sucessfully"},status=201)
            
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

            is_liked = is_post_liked(user,post_obj,'Feed')        
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

            is_liked = is_post_liked(user,post_obj,'Feed')              
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
            is_liked = is_post_liked(user,post_obj,'Feed')                
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



class LikesList(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    def post(self,request):

        serializer = PostDetailSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data
            post_obj = serializer.post_obj
            like_list = post_obj.likes.all().order_by('-created_at')


            
            page = self.paginate_queryset(like_list)
            to_send = []
            print("page is",page)

            for like_obj in page:
                user = like_obj.user

                full_name = str(user.first_name)+" " +str(user.last_name)
                thumbnail = user.profile_photo.url
           
                to_add = {
                    "thumbnail":thumbnail,
                    "full_name":full_name,
                    "user_id":user.id,
                    
                }

                to_send.append(to_add)


            print("to_send is",to_send)
            to_send = self.get_paginated_response(to_send)
            print("to_send is",to_send)

            return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)




class CommentsList(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    def post(self,request):

        serializer = PostDetailSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data
            post_obj = serializer.post_obj
            print("post obj is",post_obj)
            comments_list = post_obj.comments.all()
            print("comments_list is",comments_list)
            comments_list = comments_list.order_by('-created_at')
            print("comments_list 2 is",comments_list)

            
            page = self.paginate_queryset(comments_list)
            to_send = []
            print("page is",page)

            for comment_obj in page:
                user = comment_obj.user
                content = comment_obj.content

                full_name = str(user.first_name)+" " +str(user.last_name)
                thumbnail = user.profile_photo.url
                is_edited = comment_obj.is_edited
                if is_edited is True:
                    timestamp = post_obj.modified_at
                else:
                    timestamp = post_obj.created_at                    
           
                to_add = {
                    "thumbnail":thumbnail,
                    "full_name":full_name,
                    "user_id":user.id,
                    'timestamp':timestamp,
                    'is_edited':is_edited,
                    'content':content,
                    'comment_id':comment_obj.id,

                    
                }

                to_send.append(to_add)


            print("to_send is",to_send)
            to_send = self.get_paginated_response(to_send)
            print("to_send is",to_send)

            return Response({"success":True,"data":to_send.data,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)




class LikePost(APIView):
    def post(self,request):

        serializer = PostDetailSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            post_type = data['post_type']
            post_obj = serializer.post_obj

            is_liked = is_post_liked(user,post_obj,post_type)

            if is_liked is True:
                return Response({"success":False,"error":{"message":"post already liked"}},status=400)

            feed_post,group_post,activity_obj = create_activity_and_notification_object(
                        user,post_obj,post_type,'like_post')

            like_obj = Like.objects.create(user=user,feed_post=feed_post,group_post=group_post,
                )
            post_obj.no_of_likes += 1
            post_obj.save()


            
            activity_obj.like = like_obj
            activity_obj.save()

            to_send = {"like_obj_id":like_obj.id}
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

        serializer = PostDetailSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            post_obj = serializer.post_obj

            post_type = data['post_type']
            is_liked = is_post_liked(user,post_obj,post_type)

            
            if post_type == "Feed":
                feed_post = post_obj
                group_post = None
                

            if post_type == "Group":
                group_post = post_obj
                feed_post = None
                


            if is_liked is False:
                return Response({"success":False,"error":{"message":"post already unliked"}},status=400)

            like_obj = Like.objects.get(user=user,feed_post=feed_post,group_post=group_post,
                )
            to_send = {"like_obj_id":like_obj.id}

            like_obj.delete()

            post_obj.no_of_likes -= 1
            post_obj.save()            

            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)


class CreateComment(APIView):
    def post(self,request):

        serializer = CreateCommentSerailizer(data=request.data,context={'request': request})

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            post_type = data['post_type']
            content = data['content']
            post_obj =serializer.post_obj

            if post_type=='Feed':
                comment_type = 'feed_post'
            elif post_type=='Group':
                comment_type = 'group_post'                

            feed_post,group_post,activity_obj = create_activity_and_notification_object(
                        user,post_obj,post_type,'comment_post',)

            comment_obj = Comment.objects.create(user=user,feed_post=feed_post,group_post=group_post,
                content=content,comment_type=comment_type)
            post_obj.no_of_comments += 1
            post_obj.save()
            activity_obj.comment = comment_obj
            activity_obj.save()

            to_send = {"comment_id": comment_obj.id}
            return Response({"success":True,"data":to_send,"msg":"ok"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)


class UpdateComment(APIView):
    def post(self,request):

        serializer = UpdateOrDeleteCommentSerailizer(data=request.data,context={'request': request})

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            comment_obj = serializer.comment_obj 
            
            comment_obj.content = data.get('content',comment_obj.content)
            comment_obj.is_edited = True
            comment_obj.save()

            
            to_send = {"comment_id": comment_obj.id}
            return Response({"success":True,"data":to_send,"msg":"comment updated successfully"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)


class DeleteComment(APIView):
    def post(self,request):

        serializer = UpdateOrDeleteCommentSerailizer(data=request.data,context={'request': request})

        if serializer.is_valid():
            user = request.user    
            data = serializer.data 
            comment_obj = serializer.comment_obj 
            if comment_obj.comment_type == "feed_post":
                post_obj = comment_obj.feed_post
            elif comment_obj.comment_type == "group_post":
                post_obj = comment_obj.group_post

            
            to_send = {"comment_id":comment_obj.id}

           
            post_obj.no_of_comments -= 1
            post_obj.save()

            comment_obj.delete()            


            return Response({"success":True,"data":to_send,"msg":"comment deleted successfully"},status=200)

        if serializer.errors:          
            errors = serializer.errors
            print("error is ",errors)
            if errors.get('non_field_errors',None) is not None:
                error = {"message":errors['non_field_errors'][0]}            
            return Response({"success":False,"error":error},status=400)
