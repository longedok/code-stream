from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'code_stream/index.html'