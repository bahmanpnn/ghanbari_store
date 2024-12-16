from django.contrib import admin
from .models import OrderBasket,OrderDetail


admin.site.register(OrderBasket)
admin.site.register(OrderDetail)