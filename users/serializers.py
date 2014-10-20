from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from rest_framework import serializers
from users.models import UserInfo


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError(_("There're no users with this username/password combination"))
        return attrs


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, required=True)
    password2 = serializers.CharField(max_length=100, required=True)

    def validate_username(self, attrs, source):
        same_user = User.objects.filter(is_active=True, username__iexact=attrs['username'])
        if same_user.exists():
            raise serializers.ValidationError(_("There's already a user registered with this username"))
        return attrs

    def validate_password2(self, attrs, source):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(_("Passwords don't match"))
        return attrs


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('github_profile',)


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'info')