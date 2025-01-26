from django.contrib import admin
from .models import Product,ProductImage,ProductOfTheWeek


class ProductAdmin(admin.ModelAdmin):
    list_display=['title','slug','price','is_active','price_with_discount']


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductOfTheWeek)