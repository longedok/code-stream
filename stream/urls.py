from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<username>\w+)/$', views.ChannelView.as_view(), name='stream-channel')
]