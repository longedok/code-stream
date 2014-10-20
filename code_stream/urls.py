from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from stream.views import StreamViewSet, StreamSeriesViewSet, TechnologyViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'streams', StreamViewSet)
router.register(r'streamseries', StreamSeriesViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'users', TechnologyViewSet)

api_patterns = patterns('',
    url(r'^chat/', include('chat.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^', include(router.urls))
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='stream/index.html'), name='home'),
    url(r'^profile/$', TemplateView.as_view(template_name='profile.html'), name='profile'),
    url(r'^api/', include(api_patterns))
)