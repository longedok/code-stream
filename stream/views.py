from django.views.generic import TemplateView


class ChannelView(TemplateView):
    template_name = "streams/stream.html"