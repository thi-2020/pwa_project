from django.shortcuts import render

# Create your views here.
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from .models import *
from .serializers import *
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
from .permissions import IsOwnerOnly
from django.utils import timezone
from cassandra.cqlengine.query import BatchQuery  


class CreatePost(APIView):
    def post(self, request, format='json'):
        user = request.user
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():    
            data = serializer.data 
            post = data['post']
            
            today = timezone.now()
            added_date = today.date()
            added_date = str(added_date)
            print("added date is",added_date)

            post_obj = Post(user_id = user.id,content = post,created_date=added_date)
            post_obj.save()
            post_id = post_obj.post_id

            latest_post_obj = LatestPost(post_id = post_id,user_id=user.id,content=post,created_date=added_date)
            post_by_user_obj = PostByUser(post_id = post_id,user_id=user.id,content=post)
            latest_post_obj.save()
            post_by_user_obj.save()
            return Response({"post_id":post_id}, status=status.HTTP_201_CREATED)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class GetPostListView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id',None)
        print("user id is",user_id)
        if user_id is None:
            return Response({"message": "user_id field is empty"},status=400)
        try:
            user = User.objects.get(id=user_id)
        except Exception as e :
            return Response({"message": "User with id `{}` not found.".format(user_id)},status=404)
        posts_list = PostByUser.objects(user_id = user_id)
        serializer = PostViewSerializer(posts_list, many=True)
        return Response({"articles": serializer.data},status=200)

class GetPostDetailView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id',None)
        post_id = data.get('post_id',None)
        if user_id is None:
            return Response({"message": "user_id field is empty"},status=400)
        if post_id is None:
            return Response({"message": "post_id field is empty"},status=400)

        try:
            user = User.objects.get(id=user_id)
        except Exception as e :
            print("error is",e)
            return Response({"message": "User with id `{}` not found.".format(user_id)},status=404)           

        try:
            post = Post.objects.get(post_id = post_id)
        except Exception as e :
            print("error in post is",e)
            return Response({"message": "Post with id `{}` not found.".format(post_id)},status=404)

        serializer = PostViewSerializer(post)
        return Response({"articles": serializer.data})


class DeletePost(APIView):
    permission_classes = [IsAuthenticated,IsOwnerOnly]
    def post(self, request):

        user = request.user
        serializer = PostDeleteOrUpdateSerializer(data=request.data,context={'request': request})
        
        if serializer.is_valid(): 
            data = serializer.data
            post_obj = serializer.post_obj           
            post_id = data['post_id']

            created_date = post_obj.created_date
            user_id = post_obj.user_id

            post_obj_delete = post_obj.delete() 
            

            latest_post_list =  LatestPost.objects.filter(created_date=created_date)
            latest_post_obj = latest_post_list.filter(post_id=post_id).first()
            latest_post_obj.delete() 
            print("latest post is",latest_post_obj)

            post_by_user_list =  PostByUser.objects.filter(user_id=user_id)
            post_by_user_obj = post_by_user_list.filter(post_id=post_id).first()
            post_by_user_obj.delete()             
            return Response({"message": "Post with id `{}` has been deleted.".format(post_id)},status=204)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


        
class UpdatePost(APIView):
    permission_classes = [IsAuthenticated,IsOwnerOnly]
    def post(self, request):
        # Get object with this pk
        user = request.user
        print("user is ",user)
        serializer = PostDeleteOrUpdateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            print("came after seriailizer valid")
            data = serializer.data
            post_obj = serializer.post_obj
            post = data['post']
            post_id = data['post_id']
            created_date = post_obj.created_date
            user_id = post_obj.user_id
            post_obj = post_obj.update(content=post)
            print("cane in @133")

            latest_post_list =  LatestPost.objects.filter(created_date=created_date)
            latest_post_obj = latest_post_list.filter(post_id=post_id).first()
            latest_post_obj.update(content=post)
            print("latest post is",latest_post_obj)

            post_by_user_list =  PostByUser.objects.filter(user_id=user_id)
            post_by_user_obj = post_by_user_list.filter(post_id=post_id).first()
            post_by_user_obj.update(content=post)

                    
            return Response({"message": "Post with id `{}` has been updated.".format(post_id)},status=204)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    
        



class GetFeed(APIView):
    def get(self,request):
        posts_list = LatestPost.objects.all()
        serializer = FeedSerializer(posts_list, many=True)
        return Response({"articles": serializer.data},status=200)

