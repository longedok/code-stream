import json
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import CursorPagination
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from code_stream.pagination import CustomCursorPagination
from stream.api.serializers import (StreamSerializer, ActiveStreamSerializer, TechnologySerializer, SeriesSerializer,
                                    MaterialSerializer, EventSerializer)
from stream.models import ActiveStream, Technology, Series, Material, Event
from stream.tasks import start_stream


def publish_event():
    message = json.dumps({'action': 'events-updated'})

    RedisPublisher(facility='main', broadcast=True).publish_message(RedisMessage(message))


class StreamsViewset(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = ActiveStream.objects.select_related('stream__owner__info')
    serializer_class = ActiveStreamSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ActiveStreamSerializer
        elif self.action == 'create':
            return StreamSerializer

    def perform_create(self, serializer):
        user = self.request.user
        stream = serializer.save(owner=user)

        Event.objects.create(user=user, type=Event.STREAM_STARTED, description='streaming.')
        publish_event()

        start_stream.delay(stream.pk, user.pk, user.info.twitch_channel)

    @list_route(methods=['GET'])
    def get_active(self, request):
        username = request.query_params.get('username')

        try:
            stream = ActiveStream.objects.get(stream__owner__username=username)
        except ActiveStream.DoesNotExist:
            raise Http404()

        return Response(ActiveStreamSerializer(stream).data, status=status.HTTP_200_OK)


class SeriesViewSet(ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TechnologyViewSet(ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

    def perform_create(self, serializer):
        technology = serializer.save(creator=self.request.user)

        Event.objects.create(user=self.request.user, type=Event.TECHNOLOGY_ADDED,
                             description='new technology "%s".' % technology.title)
        publish_event()


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def perform_create(self, serializer):
        material = serializer.save(creator=self.request.user)

        Event.objects.create(user=self.request.user, type=Event.MATERIAL_ADDED,
                             description='new technology material "%s".' % material.title)
        publish_event()


class EventsView(ListModelMixin, GenericViewSet):
    queryset = Event.objects.all().order_by('-created')
    serializer_class = EventSerializer

    pagination_class = CustomCursorPagination
    page_size = 10