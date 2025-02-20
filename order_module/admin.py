from django.contrib import admin
from .models import OrderBasket,OrderDetail,Coupon

# class OrderBasketAdmin(admin.ModelAdmin):
#     list_display=['user','is_paid','payment_date','discount']

# class OrderDetailAdmin(admin.ModelAdmin):
#     list_display=['product','order_basket','count','final_price']

# admin.site.register(OrderBasket,OrderBasketAdmin)
# admin.site.register(OrderDetail,OrderDetailAdmin)



class OrderDetailAdminInline(admin.TabularInline):
    model = OrderDetail
    list_display=['product','order_basket','count','final_price']


class OrderBasketAdmin(admin.ModelAdmin):
    list_display=['user','is_paid','payment_date']
    inlines=[OrderDetailAdminInline]

admin.site.register(OrderBasket,OrderBasketAdmin)
admin.site.register(Coupon)