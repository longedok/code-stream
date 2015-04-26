from django.views.generic import ListView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from stream.models import Technology, ActiveStream, Stream
from stream.serializers import TechnologySerialzier, StreamSerializer

from tasks import start_stream


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerialzier


class IndexView(ListView):
    model = ActiveStream
    template_name = 'stream/index.html'


class StreamsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = StreamSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user

            stream = serializer.save(owner=user)
            start_stream.delay(stream.pk, user.info.twitch_channel)

            return Response(StreamSerializer(stream).data, status=status.HTTP_200_OK)

    def get(self, request):
        return Response(StreamSerializer(Stream.objects.active(), many=True).data, status=status.HTTP_200_OK)
