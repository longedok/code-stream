from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import LoginSerializer, UserSerializer, RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username, password = serializer.validated_data['username'], serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return Response({'data': UserSerializer(user).data})


class RegisterView(GenericAPIView):
    def post(self, request):
        srlzr = RegisterSerializer(data=request.data)
        if srlzr.is_valid(raise_exception=True):
            user = srlzr.save()
            #User.objects.create_user(data['username'], data['email'], data['password'])
            user = authenticate(username=user.username, password=user.password)
            if user is not None:
                login(request, user)
            else:
                return Response({'data': {'non_field_errors': "Your account has been created, but we failed to "
                                                              "automatically log you in. Use log in form on the "
                                                              "frontpage to log in manually."}},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'data': UserSerializer(user).data})


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=200)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')