from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from stream.views import IndexView

api_patterns = patterns('',
    url(r'^chat/', include('chat.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^streams/', include('stream.urls'))
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^profile/$', TemplateView.as_view(template_name='profile.html'), name='profile'),
    url(r'^api/', include(api_patterns))
)