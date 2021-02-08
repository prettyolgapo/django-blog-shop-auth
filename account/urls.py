from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
   path('my_login', views.my_login, name='my_login'),

]