from rest_framework import serializers
from .models import *
from django.core import exceptions
from django.conf import settings



CATEGORY_CHOICES = (
    ('Nomral','Normal'),
    ('Group','Group'),
    ('Event','Event')
)
class PostCreateSerializer(serializers.Serializer):
    post = serializers.CharField(max_length=settings.POST_MAX_LENGTH,required=True)
    category_id = serializers.CharField(max_length=10,required=True)



class PostViewSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=settings.POST_MAX_LENGTH)
    post_id = serializers.CharField(max_length=300)
    user_id = serializers.CharField(max_length=300)
    created_at = serializers.DateTimeField()
    first_name = serializers.CharField(max_length=300)
    last_name = serializers.CharField(max_length=300)
    category_id = serializers.CharField(max_length=30)
    no_of_likes = columns.Integer()
    no_of_comments = columns.Integer()


class FeedSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=settings.POST_MAX_LENGTH)
    post_id = serializers.CharField(max_length=300)
    user_id = serializers.CharField(max_length=300)
    created_datetime = serializers.DateTimeField()

class PostDeleteOrUpdateSerializer(serializers.Serializer):
    post_id = serializers.CharField(max_length=300)
    post = serializers.CharField(max_length=settings.POST_MAX_LENGTH,required=False)
    

    def validate(self, data):
        post_id = data.get('post_id')
        request = self.context.get('request')
        user = request.user

        try:
            # post_obj = Post.objects.filter(post_id=post_id).first()
            post_obj = Post.objects.get(post_id=post_id)
            if post_obj is None:
                raise ValueError("not present")
        except Exception as e:
            raise serializers.ValidationError("post with {} not found ".format(post_id))
        print("post_obj is",post_obj)
        print("post object usre id is",post_obj.user_id)
        print("user id is",user.id)
        if post_obj.user_id != user.id:
            raise serializers.ValidationError("Not authorized to perform this operation")

        self.post_obj = post_obj

        return data


 