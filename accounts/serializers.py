from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import *
from django.core import exceptions
import django.contrib.auth.password_validation as validators



class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=150,required=True)
    first_name = serializers.CharField(max_length=150,required=True)
    last_name = serializers.CharField(max_length=150,required=True)
    dob = serializers.DateField()

    # first_name = serializers.CharField(max_length=150)
    # last_name = serializers.CharField(max_length=150)

 


    def validate(self, data):
        print("@25")
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        qs1 = User.objects.filter(email = email).exists()
        qs2 = User.objects.filter(phone = phone).exists()
        print("qs1 is",qs1)
        print("qs2 is",qs2)

        errors = dict() 
        if qs1 is True:
            errors['email'] = "email already exists"

        if qs2 is True:
            errors['phone'] = "Phone already exists"

        try:

             # validate the password and catch the exception
            validators.validate_password(password=password)

         # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

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