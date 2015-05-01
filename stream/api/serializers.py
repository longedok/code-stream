from rest_framework import serializers

from stream.models import Stream, ActiveStream
from users.api.serializers import UserSerializer


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream


class ActiveStreamSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='stream.owner')
    title = serializers.ReadOnlyField(source='stream.title')
    started = serializers.ReadOnlyField(source='stream.created')

    class Meta:
        model = ActiveStream
        fields = ('id', 'user', 'title', 'viewers', 'started', 'preview_url')