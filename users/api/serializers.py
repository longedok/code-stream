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
            raise serializers.ValidationError(_("Wrong username or password."))
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, required=True)
    password2 = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        validated_data.pop('password2')
        return super(RegisterSerializer, self).create(validated_data)

    def validate_username(self, value):
        same_user = User.objects.filter(is_active=True, username__iexact=value)
        if same_user.exists():
            raise serializers.ValidationError(_("Username is taken. Choose another one."))

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(_("Passwords don't match"))
        return attrs


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('github_profile', 'twitch_channel')


class UserSerializer(serializers.ModelSerializer):
    from stream.api.serializers import SeriesSerializer
    info = UserInfoSerializer()
    series = SeriesSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'info', 'series')