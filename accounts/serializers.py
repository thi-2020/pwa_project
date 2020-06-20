from rest_framework import exceptions,serializers
from rest_framework.validators import UniqueValidator
from accounts.models import *
import django.contrib.auth.password_validation as validators

from django.contrib.auth import authenticate


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all(),message = 'email already exists')]
            
            )

    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150,required=True,
                validators=[UniqueValidator(queryset=User.objects.all(),message = 'username already exists')]
                 )
    phone = serializers.CharField(max_length=10,min_length=10,required=True,
                validators=[UniqueValidator(queryset=User.objects.all(),message = 'phone number already exists')]
                # validators=[UniqueValidator(queryset=UserProfile.objects.filter(user__phone_verfied=True),message = 'phone number already exists')]
                           )

    username = serializers.CharField(max_length=150,required=True)
    dob = serializers.DateField()
    key = serializers.CharField(max_length=150,required=False)
    last_name = serializers.CharField(max_length=150,required=False)
    first_name = serializers.CharField(max_length=150)





    def validate(self, data):
        password = data.get('password')
       

        phone = data.get('phone')

        
                

        errors = dict() 
        if phone.isdigit() is False:
            errors['phone'] = 'should be numbers only'
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)


        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        print("attres is",attrs)
        authenticate_kwargs = {
            'username':attrs['username'],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        print("keyword argements is ",authenticate_kwargs)
        self.user = authenticate(**authenticate_kwargs)
        print("user is ",self.user)

        if self.user is None :
            raise exceptions.AuthenticationFailed(

                'invalid credentails',
            )

        return attrs





class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ['user']




