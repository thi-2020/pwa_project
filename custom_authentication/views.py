from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import *
from .authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import APIView

# class TokenViewBase(generics.GenericAPIView):
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny



class TokenObtainPairView(APIView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    permission_classes = [AllowAny,]

    def post(self, request, format='json'):
        print("request.user is",request.user)
        print("request.data in @24 in views.py of cust_auth is",request.data)
        serializer = TokenObtainPairSerializer(data=request.data)
        
        data=request.data
        email= data['email']
        print("email is",email)
        if serializer.is_valid():
            print("serailizer data",serializer.data)
            data = serializer.validated_data
            access = data['access']
            user = serializer.user
            to_send = dict()            


            to_send['user_id'] = user.id            
            to_send['first_name'] = user.first_name
            to_send['last_name'] = user.last_name
            to_send['email'] = user.email
            to_send['phone'] = user.phone
            to_send['dob'] = str(user.dob)
            to_send['access'] = access
            return Response(to_send, status=status.HTTP_200_OK)

            # try:
            #     print("@29 ")    
            #     serializer.is_valid()
            # except TokenError as e:
            #     raise InvalidToken(e.args[0])

        return Response(serializer.errors, status=status.HTTP_200_OK)