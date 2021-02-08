from django.contrib import admin
from .models import Product, OrderItem, Cart, Point

admin.site.register(Product)
admin.site.register(Point)
admin.site.register(Cart)
admin.site.register(OrderItem)

