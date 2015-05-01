from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.StreamsView.as_view(), name='stream-streams')
]