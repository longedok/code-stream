import json

from django.views.generic import TemplateView
from rest_framework.renderers import JSONRenderer
from stream.api.serializers import ActiveStreamSerializer
from stream.models import ActiveStream
from users.api.serializers import UserSerializer


class AngularServiceBuilder(object):
    data_service_start = "app.service('%(service_name)s', function() {\n"
    property_definition = "\tthis.%(name)s = JSON.parse('%(value)s');\n"
    data_service_end = "});\n"

    def __init__(self, service_name):
        self.built_code = self.data_service_start % {'service_name': service_name}

    def add_property(self, name, value):
        self.built_code += self.property_definition % {'name': name, 'value': value}

    def get_result(self):
        self.built_code += self.data_service_end
        return self.built_code


class MainView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        user = self.request.user
        code_builder = AngularServiceBuilder('BackendData')

        if user.is_authenticated():
            user_serialized = UserSerializer(user).data
            user_serialized['is_authenticated'] = True
            user_repr = JSONRenderer().render(user_serialized)
        else:
            user_repr = json.dumps({'is_authenticated': False})

        streams_serialized = ActiveStreamSerializer(ActiveStream.objects.select_related('stream__owner__info'),
                                                    many=True).data
        streams_repr = JSONRenderer().render(streams_serialized)

        code_builder.add_property('user', user_repr)
        code_builder.add_property('streams', streams_repr)

        context['backend_data_service_code'] = code_builder.get_result()

        return context