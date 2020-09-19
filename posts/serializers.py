from rest_framework import serializers
from .models import *
from django.core import exceptions
from django.conf import settings

from accounts.models import VisibilitySettings


def check_post(post_id,post_type):
    is_error_occured = False
    error_msg = ""

    if post_id is None:
        error_msg = "post_id not present"
        return (True,error_msg,None)


    if post_type is None:
        error_msg = "post_type not present"
        return (True,error_msg,None)



    if post_type not in ['Feed','Group']:
        error_msg = "invalid post_type"
        return (True,error_msg,None)

    if post_type == 'Feed':
        try:
            post_obj = FeedPost.objects.get(id=post_id)
        except Exception as e:
            error_msg = "post not found"
            return (True,error_msg,None)


    if post_type == 'Group':
        try:
            post_obj = GroupPost.objects.get(id=post_id)
        except Exception as e:
            error_msg = "post not found"
            return (True,error_msg,None)
            

    return (is_error_occured,error_msg,post_obj)


class PostCreateSerializer(serializers.Serializer):
    content = serializers.CharField(required=False)
    visibilty_status = serializers.CharField(required=False)
    image = serializers.FileField(required=False)


    def validate(self, data):

        content = data.get('content',None)
        image = data.get('image',None)
        visibilty_status = data.get('visibilty_status',None)

        if content is None and image is None:
            raise serializers.ValidationError("Empty post not allowed")

        if visibilty_status is None:
            raise serializers.ValidationError("visibilty_status is not present")
        

        types = VisibilitySettings().types
        
        print("types is",types)
        types = [item[0] for item in types]

        print("visibilty_status is ",visibilty_status)
        if visibilty_status not in  types:
            raise serializers.ValidationError("invalid visibilty_status")

        if content is not None:
            if len(content)>settings.POST_MAX_LENGTH:
                raise serializers.ValidationError("Post is too long")

        return data


class PostUpdateOrDeleteSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=False)
    post_type = serializers.CharField(required=False)
    content = serializers.CharField(max_length=settings.POST_MAX_LENGTH,required=False)
    visibilty_status = serializers.CharField(required=False)
    image = serializers.FileField(required=False)


    def validate(self, data):
        #checks in order
        request = self.context.get('request')
        user = request.user
        print('user is',user) 
        post_id = data.get('post_id',None)
        post_type = data.get('post_type',None)
        content = data.get('content',None)
        image = data.get('image',None)
        visibilty_status = data.get('visibilty_status',None)

        is_error_occured,error_msg,post_obj = check_post(post_id,post_type)

        if is_error_occured is True:
            raise serializers.ValidationError(error_msg)


        types = VisibilitySettings().types
        
        
        types = [item[0] for item in types]
        print("types is",types)

        if visibilty_status is not None:
            print("visibilty_status is ",visibilty_status)
            if visibilty_status not in  types:
                raise serializers.ValidationError("invalid visibilty_status")

        self.post_obj = post_obj

        if post_obj.user != user:
            raise serializers.ValidationError("Unauthorized to perform this action")



        if content is not None:
            if len(content)>settings.POST_MAX_LENGTH:
                raise serializers.ValidationError("Post is too long")

        return data






class PostDetailSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=False)
    post_type = serializers.CharField(required=False)


    def validate(self, data):
        
        post_id = data.get('post_id',None)
        post_type = data.get('post_type',None)
        print("post_id is",post_id)
        print("post_type is",post_type)
        is_error_occured,error_msg,post_obj = check_post(post_id,post_type)

        if is_error_occured is True:
            raise serializers.ValidationError(error_msg)




        self.post_obj = post_obj
        return data



class CreateCommentSerailizer(serializers.Serializer):
    post_id = serializers.IntegerField(required=False)
    post_type = serializers.CharField(required=False)    
    content = serializers.CharField(required=False)    


    def validate(self, data):
        #checks in order
        
        request = self.context.get('request')
        user = request.user
        print('user is',user)
        post_id = data.get('post_id',None)
        post_type = data.get('post_type',None)        

        content = data.get('content',None)
        is_error_occured,error_msg,post_obj = check_post(post_id,post_type)

        if is_error_occured is True:
            raise serializers.ValidationError(error_msg)

        


        self.post_obj = post_obj

        if post_obj.is_comment_disabled is True:
            raise serializers.ValidationError("Comments on this post are disabled")

        if content is None:
            raise serializers.ValidationError("Empty comment not allowed")


        if content is not None:
            if len(content)>settings.POST_MAX_LENGTH:
                raise serializers.ValidationError("Comment is too long")

        return data




class UpdateOrDeleteCommentSerailizer(serializers.Serializer):
    comment_id = serializers.IntegerField(required=False)   
    content = serializers.CharField(required=False)    


    def validate(self, data):
        #checks in order
        request = self.context.get('request')
        user = request.user
        print('user is',user)        
        comment_id = data.get('comment_id',None)
        content = data.get('content',None)
        if comment_id is None:
            raise serializers.ValidationError("comment_id not present")


        if content is not None:
            if len(content)>settings.POST_MAX_LENGTH:
                raise serializers.ValidationError("Comment is too long")
        
        try:
            comment_obj = Comment.objects.get(id=comment_id)
        except Exception as e:
            error_msg = "Comment not found"
            raise serializers.ValidationError(error_msg)

        if comment_obj.user == user:
            raise serializers.ValidationError("Unauthorized to perform this action")




        self.comment_obj = comment_obj
        return data        