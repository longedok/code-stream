from rest_framework import serializers

from stream.models import Stream, ActiveStream, Technology, Series, Material, Event


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        read_only_fields = ('owner', 'created', 'finished')


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        read_only_fields = ('owner', 'created', 'modified')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'created', 'modified', 'title', 'url', 'description', 'technology')
        read_only_fields = ('creator', 'created', 'modified')


class TechnologySerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, required=False)

    class Meta:
        model = Technology
        fields = ('id', 'title', 'description', 'creator', 'created', 'modified', 'materials')
        read_only_fields = ('creator', 'created', 'modified', 'materials')


class ActiveStreamSerializer(serializers.ModelSerializer):
    from users.api.serializers import UserSerializer
    user = UserSerializer(source='stream.owner')
    title = serializers.ReadOnlyField(source='stream.title')
    started = serializers.ReadOnlyField(source='stream.created')
    technologies = TechnologySerializer(many=True, source='stream.technologies')

    class Meta:
        model = ActiveStream
        fields = ('id', 'user', 'title', 'viewers', 'started', 'preview_url', 'technologies')


class EventSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    action = serializers.SerializerMethodField()

    def get_action(self, obj):
        if obj.type in (Event.MATERIAL_ADDED, Event.TECHNOLOGY_ADDED):
            return 'added'
        elif obj.type == Event.STREAM_STARTED:
            return 'started'
        elif obj.type == Event.STREAM_FINISHED:
            return 'finished'

        return ''

    class Meta:
        model = Event
        fields = ('id', 'created', 'username', 'type', 'action', 'description')