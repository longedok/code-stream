from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import LoginSerializer, UserSerializer, RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        srlzr = LoginSerializer(data=request.DATA)
        if srlzr.is_valid():
            username, password = srlzr.object['username'], srlzr.object['password']
            # we check that authenticate returns a valid user in the serializer validation methods
            user = authenticate(username=username, password=password)
            login(request, user)
            return Response({'data': UserSerializer(user).data})
        else:
            return Response(srlzr.errors, status=400)


class RegisterView(APIView):
    def post(self, request):
        srlzr = RegisterSerializer(data=request.DATA)
        if srlzr.is_valid():
            data = srlzr.object
            User.objects.create_user(data['username'], data['email'], data['password'])
            user = authenticate(username=data['username'], password=data['password'])
            login(request, user)
            return Response({'data': UserSerializer(user).data})
        else:
            return Response(srlzr.errors, status=400)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=200)