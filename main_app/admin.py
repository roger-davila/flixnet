from django.contrib import admin
from .models import Order, OrderDetail, ShippingAddress, Movie

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Movie)
