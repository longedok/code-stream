from rest_framework import serializers

from stream.models import Stream, ActiveStream, Technology, Series


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        read_only_fields = ('owner', 'created', 'modified')


class ActiveStreamSerializer(serializers.ModelSerializer):
    from users.api.serializers import UserSerializer
    user = UserSerializer(source='stream.owner')
    title = serializers.ReadOnlyField(source='stream.title')
    started = serializers.ReadOnlyField(source='stream.created')

    class Meta:
        model = ActiveStream
        fields = ('id', 'user', 'title', 'viewers', 'started', 'preview_url')