from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import *
from django.core import exceptions
import django.contrib.auth.password_validation as validators

from datetime import timedelta

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=150,required=True)
    first_name = serializers.CharField(max_length=150,required=True)
    last_name = serializers.CharField(max_length=150,required=True)
    username = serializers.CharField(max_length=150,required=True)
    dob = serializers.DateField()
    key = serializers.CharField(max_length=150,required=True)

    # first_name = serializers.CharField(max_length=150)
    # last_name = serializers.CharField(max_length=150)

 


    def validate(self, data):
        print("@25")
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        username = data.get('username')
        qs1 = User.objects.filter(email = email).exists()
        qs2 = User.objects.filter(phone = phone).exists()
        qs3 = User.objects.filter(username = username).exists()
        print("qs1 is",qs1)
        print("qs2 is",qs2)


        errors = dict() 

        try:
            invitation_obj = Invitation.objects.get(key = key)
        except Exception as e:
            print("error is ",e)
            errors['key'] = 'invalid key'
        if invitation_obj.email != email:
            errors['email'] = 'Your email is not in the invitation list'

    
        if qs1 is True:
            errors['email'] = "email already exists"

        if qs2 is True:
            errors['phone'] = "Phone already exists"

        if qs3 is True:
            errors['username'] = "Username already exists"

        try:

             # validate the password and catch the exception
            validators.validate_password(password=password)

         # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        self.invitation_obj = invitation_obj
        return super(UserSerializer, self).validate(data)







    # def validate(self, data):
    #     print("@28 in userserializer in accounts")
    #     queryset=User.objects.filter(email_verfied=True)
    #     print("queryset is",queryset)
    #      # here data has all the fields which have validated values
    #      # so we can create a User instance out of it
    #     # user = User(**data)
    #     queryset=UserProfile.objects.filter(user__phone_verfied=True)
    #     print("qs for phone -nukmbers is ",queryset)
    #      # get the password from the data
    #     password = data.get('password')

    #     errors = dict() 
    #     try:

    #          # validate the password and catch the exception
    #         validators.validate_password(password=password)

    #      # the exception raised here is different than serializers.ValidationError
    #     except exceptions.ValidationError as e:
    #         errors['password'] = list(e.messages)

    #     if errors:
    #         raise serializers.ValidationError(errors)

    #     return super(UserSerializer, self).validate(data)

class InvitationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        print("@25")
        email = data.get('email')
        request = self.context.get('request')
        user = request.user
        errors = dict() 
  
        qs1 = User.objects.filter(email = email).exists()
        qs2 = Invitation.objects.filter(email = email).exists()
        sent_threshold = timezone.now() - timedelta(days = 7)
        print("sent threshold is ",sent_threshold)
        count = Invitation.objects.filter(sender_id = user.id).filter(created__gt = sent_threshold).count()
        print("count is ",count)
        if count >= 10:
            errors['email'] = "you have reached your limit of 5 monthly invitations"
        if qs1 is True:
            errors['email'] = "An active user is using this e-mail address"
        if qs2 is True:
            errors['email'] = "Alreday sent an invitation to this email address"

        if errors:
            raise serializers.ValidationError(errors)

        return data