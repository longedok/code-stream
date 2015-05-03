from django.views.generic import TemplateView
from stream.models import ActiveStream


class ChannelView(TemplateView):
    template_name = "streams/stream.html"

    def get_context_data(self, **kwargs):
        context = super(ChannelView, self).get_context_data(**kwargs)

        username = self.kwargs['username']
        active_stream = ActiveStream.objects.get(stream__owner__username=username)

        context['stream'] = active_stream.stream

        return context