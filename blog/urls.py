from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from .views import ContactView, SearchResultsView
# from .views import SearchResultsView


app_name = 'blog'
urlpatterns = [
   #url(r'^$', views.post_list, name='post_list'),  # for redirect from http://127.0.0.1:8000/blog
   url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
   url(r'^post/new/$', views.post_new, name='post_new'),
   url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
   path('index', views.index, name='home'),
   # path('login', TemplateView.as_view(template_name="blog/login_prev.html")),
   path('about', TemplateView.as_view(template_name="blog/about.html"), name='about'),
   path('contact', ContactView.as_view(), name='contact'),
   # path('contact', views.get_name, name='contact'),
   path('thanks/', TemplateView.as_view(template_name="blog/thanks.html"), name='thanks'),
   path('search/', SearchResultsView.as_view(), name='search_results'),
   path('', views.post_list, name='post_list'),  # for redirect from http://127.0.0.1:8000/blog

    # note: убирать .html из адресной строки /htaccess????
]
