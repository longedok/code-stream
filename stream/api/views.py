from django.http import Http404
from rest_framework import permissions, status
from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from stream.api.serializers import StreamSerializer, ActiveStreamSerializer, TechnologySerializer, SeriesSerializer, \
    MaterialSerializer
from stream.models import ActiveStream, Technology, Series, Material
from stream.tasks import start_stream


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
        serializer.save(creator=self.request.user)


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)