from django.contrib import admin
from .models import OrderBasket,OrderDetail,Coupon,Checkout

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
    list_display=['user','is_paid','payment_date','get_total_amount','coupon']
    inlines=[OrderDetailAdminInline]

class CheckOutAdmin(admin.ModelAdmin):
    list_display=['__str__','user','is_successfull','created_at']

admin.site.register(OrderBasket,OrderBasketAdmin)
admin.site.register(Coupon)
admin.site.register(Checkout,CheckOutAdmin)