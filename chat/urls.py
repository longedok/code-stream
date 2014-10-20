from django.conf.urls import patterns, url

urlpatterns = patterns('chat.views',
    url(r'^post$', 'post', name='chat-post')
)