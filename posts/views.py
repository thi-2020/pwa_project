from django.shortcuts import render,get_object_or_404

# Create your views here.




from .models import *
from .serializers import *
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




class OwnPostView(APIView):
    def get(self, request):
        user = request.user

        posts = NormalPost.objects.filter(user=user).values()
        return Response({"posts": posts},status=200)


    def get(self,request,post_id):
        user = request.user
        
        post = NormalPost.object.get(id=post_id).values()
        return Response({"posts": post},status=200)

    def post(self,request):
        user = request.user
        serializer = PostCreateSerializer(data=request.data)

        if serializer.is_valid():    
            data = serializer.data 
            content = data['content']
            
            post_obj = NormalPost.objects.create(user=user,content=content)

            return Response({"post_id": post_obj.id},status=201)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,pk):
        user = request.user
        serializer = PostCreateSerializer(data=request.data)


    # def put(self, request, pk):
    #     user = request.user
    #     saved_article = get_object_or_404(NormalPost.objects.all(user=user), pk=pk)
    #     data = request.data.get('article')
    #     serializer = PostCreateSerializer(instance=saved_article, data=data, partial=True
    #     if serializer.is_valid(raise_exception=True):
    #         article_saved = serializer.save()
    #     return Response({"success": "Article '{}' updated successfully".format(article_saved.title)})



        if serializer.is_valid():    
            data = serializer.data 
            content = data['content']

            post_obj = NormalPost.objects.create(user=user,content=content)

            return Response({"post_id": post_obj.id},status=201)

        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    





class OtherPostView(APIView):
    def get(self,request,user_id):

        user = User.objects.get(id=user_id)
        posts = NormalPost.objects.filter(user=user).values()

        return Response({"posts": posts},status=200)

    def get(self,request,user_id,post_id):
        post = NormalPost.object.get(id=post_id).values()
        return Response({"posts": post},status=200)
