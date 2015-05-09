from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^post/(?P<username>\w+)/$', views.post,  name='chat-post')
]