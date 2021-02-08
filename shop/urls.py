from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from .views import SearchResultsView, CheckoutView

app_name = 'shop'
urlpatterns = [
    path('', views.shop_list, name='list'),  # for redirect from http://127.0.0.1:8000/shop
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('thanks/', views.thanks, name='thanks'),
    path('order_complete/', views.order_complete, name='order-complete'),
    url(r'^cart-update/(?P<pk>\d+)/$', views.cart_update, name='cart-update'),
    url(r'^item-remove/(?P<pk>\d+)/$', views.item_remove, name='item-remove'),
    url(r'^add/(?P<pk>\d+)/$', views.add_to_cart, name='add-to-cart'),
    url(r'^details/(?P<pk>\d+)/$', views.product_details, name='product-details'),


]
