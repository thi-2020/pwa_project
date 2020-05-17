from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, authentication

from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

from rest_framework_simplejwt.settings import api_settings

from accounts.models import User
AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)


class JWTAuthentication(authentication.BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        print("@28 in authenticate in authentication.py")
        header = self.get_header(request)
        print("header is ",header)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        print("raw token is ",raw_token)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        print("validated token is",validated_token)
        user = self.get_user(validated_token)
        # user.is_authenticated = True
        request.user = user
        return user, validated_token

    def authenticate_header(self, request):
        print("@42 in authenticate in authentication.py")
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get('HTTP_AUTHORIZATION')
        print("@54 in get_header in authentication.py")
        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        print("@66 in get_raw_token in authentication.py")
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _('Authorization header must contain two space-delimited values'),
                code='bad_authorization_header',
            )

        return parts[1]

    def get_validated_token(self, raw_token):

        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """

        print("@92 in get_validated_token in authentication.py")
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        print("@111 in get_user in authentication.py")
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))
        print("user id",user_id) 
        try:
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        # if not user.is_active:
        #     raise AuthenticationFailed(_('User is inactive'), code='user_inactive')
        print("user is cfghdgh ",user)
        return user



