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
    dob = serializers.DateField()
    key = serializers.CharField(max_length=150,required=False)
    last_name = serializers.CharField(max_length=150,required=False)
    first_name = serializers.CharField(max_length=150)





    def validate(self, data):
        password = data.get('password')
       

        phone = data.get('phone')
        email = data.get('email')
        key = data.get('key')
        errors = dict() 
        try:
            invitation_obj = Invitation.objects.get(invitation_key = key)
            print("invitation_obj.receiver_email  is",invitation_obj.receiver_email )
            if invitation_obj.receiver_email is not None and invitation_obj.receiver_email != email:
                errors['email'] = 'Your email is not in the invitation list'
        
            if invitation_obj.receiver_phone is not None and invitation_obj.receiver_phone != phone:
                errors['phone'] = 'Your phone is not in the invitation list'



        except Exception as e:
            print("error is ",e)
            errors['key'] = 'invalid key'


        
        if phone.isdigit() is False:
            errors['phone'] = 'should be numbers only'
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)


        if errors:
            raise serializers.ValidationError(errors)
        self.invitation_obj = invitation_obj
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





class UserDetailSerailizer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)

    def validate(self, data):
        user_id = data.get('user_id')

        if user_id is None:
            raise serializers.ValidationError("user_id not present")

        try:
            user_object = User.objects.get(id=user_id)
        except Exception as e:
            raise serializers.ValidationError("user not found")


        self.user_object = user_object
        return data


