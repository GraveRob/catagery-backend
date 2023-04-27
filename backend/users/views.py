from django.contrib.auth import get_user_model, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, status


# Create your views here.

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            data = request.data
            
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (SessionAuthentication, )
    
    def post(self, request):
        serializer = UserLoginSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(request.data)
            
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    