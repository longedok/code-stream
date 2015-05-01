from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from stream.api.serializers import StreamSerializer, ActiveStreamSerializer
from stream.models import ActiveStream
from stream.tasks import start_stream


class StreamsView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = StreamSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user

            stream = serializer.save(owner=user)
            start_stream.delay(stream.pk, user.pk, user.info.twitch_channel)

            return Response(StreamSerializer(stream).data, status=status.HTTP_200_OK)

    def get(self, request):
        return Response(ActiveStreamSerializer(ActiveStream.objects.all(), many=True).data, status=status.HTTP_200_OK)