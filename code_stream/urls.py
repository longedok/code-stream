from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^$', views.MainView.as_view()),

    url(r'^api/', include([
        url(r'^streams/', include('stream.api.urls')),
        url(r'^users/', include('users.api.urls')),
        url(r'^chat/', include('chat.api.urls'))
    ])),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
