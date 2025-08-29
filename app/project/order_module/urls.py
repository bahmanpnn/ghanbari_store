from django.urls import path
from . import views


app_name="order_module"
urlpatterns = [
    path('add-product-to-basket-orders/',views.add_product_to_basket,name='add-product-to-basket'),
    path('basket/',views.UserOrderBasket.as_view(),name='order-basket'),
    # path('remove_order_detail/',views.remove_order_detail_user_basket,name='remove-order-detail-ajax'),
    path('remove_basket_card_order_detail/',views.remove_user_basket_card_order_detail,name='remove_user_basket_card_order_detail-ajax'),
    path('change_order_detail_count/',views.change_order_detail_count,name='change-order-detail-count-ajax'),
    path("apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path('checkout/',views.CheckOutView.as_view(),name="user-checkout"),
    # path('checkout/',views.checkout,name="user-checkout"),


    # path('checkout/',views.UserCheckOutBasket.as_view(),name='order-checkout'),
    # path('coupon-apply/',views.CouponApplyView.as_view(),name='coupon-apply'),
    # path('remove_product_from_basket/<int:detail_id>/',views.remove_product_from_basket,name='remove-product-from-basket'),
    # path('remove_basket_cart/<int:detail_id>/',views.remove_basket_cart,name="remove-basket-cart"),
    # path('remove_product_from_basket_ajax/',views.remove_product_from_basket_ajax,name='remove-product-from-basket-ajax'),
    # path('confirm_checkout/',views.confirm_checkout,name='confirm-checkout'),
]
