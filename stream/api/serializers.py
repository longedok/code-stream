from rest_framework import serializers

from stream.models import Stream, ActiveStream, Technology, Series, Material


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream


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


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'created', 'modified', 'title', 'url', 'description', 'technology')
        read_only_fields = ('creator', 'created', 'modified')


class TechnologySerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True)

    class Meta:
        model = Technology
        fields = ('id', 'title', 'description', 'creator', 'created', 'modified', 'materials')
        read_only_fields = ('creator', 'created', 'modified', 'materials')