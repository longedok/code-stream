from rest_framework import viewsets

from stream.models import StreamSeries, Stream, Technology
from stream.serializers import StreamSerializer, TechnologySerialzier, SeriesSerializer


class StreamSeriesViewSet(viewsets.ModelViewSet):
    queryset = StreamSeries.objects.all()
    serializer_class = SeriesSerializer


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

    def stop(self):
        pass


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerialzier