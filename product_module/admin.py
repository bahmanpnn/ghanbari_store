from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display=['title','slug','price','is_active']


admin.site.register(Product,ProductAdmin)