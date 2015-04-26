from django.conf.urls import patterns, url
from stream.views import StreamsView

urlpatterns = patterns('',
    url(r'^streams/$', StreamsView.as_view(), name='streams-list')
)