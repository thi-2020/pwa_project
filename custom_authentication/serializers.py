from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers



from rest_framework_simplejwt.tokens import RefreshToken





class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        print("attres is",attrs)
        authenticate_kwargs = {
            'email':attrs['email'],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        print("keyword argements is ",authenticate_kwargs)
        self.user = authenticate(**authenticate_kwargs)
        print("user is ",self.user)
        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None :
            raise exceptions.AuthenticationFailed(

                'invalid credentails',
            )

        return attrs

class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        print("attrs in line @48 is",attrs)
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)

        return data