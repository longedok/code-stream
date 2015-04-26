from rest_framework import serializers

from models import StreamSeries, Stream, Technology


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamSeries
        fields = ('name',)

    def pre_save(self, obj):
        obj.owner = self.request.user


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream


class TechnologySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Technology

    def pre_save(self, obj):
        obj.creator = self.request.user