from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='users-login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='users-logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='users-register')
]