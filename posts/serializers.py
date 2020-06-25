from rest_framework import serializers
from .models import *
from django.core import exceptions
from django.conf import settings




class PostCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=settings.POST_MAX_LENGTH,required=True)
    