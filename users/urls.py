from django.conf.urls import patterns, url
from users.views import LoginView, RegisterView, LogoutView

urlpatterns = patterns('users.views',
    url(r'^login/$', LoginView.as_view(), name='user-login'),
    url(r'^logout/$', LogoutView.as_view(), name='user-logout'),
    url(r'^register/$', RegisterView.as_view(), name='user-register')
)