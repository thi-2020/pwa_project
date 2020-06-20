from django.shortcuts import render

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






class PostView(APIView):
    def get(self, request):
        articles = NormalPost.objects.all()
        return Response({"posts": articles},status=200)


    def
