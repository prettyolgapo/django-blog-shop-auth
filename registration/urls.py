from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login

app_name = 'registration'
urlpatterns = [
   url(r'^login/$', LoginView.as_view(), name='login'),
   url(r'^logout/$', LogoutView.as_view(), name='logout'),
   url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
]