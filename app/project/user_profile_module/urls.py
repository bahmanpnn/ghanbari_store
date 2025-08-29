from django.urls import path
from . import views


app_name="user_profile_module"
urlpatterns = [
    path('',views.UserProfileView.as_view(),name='user-profile'),
    path('user-favorites/',views.user_favorite_products,name='user-favorite-list'),
    path('user-order-detail/<int:order_id>/',views.user_order_detail,name='user-order-detail'),
    path('remove_user_favorite_product/',views.remove_user_favorite_product,name='remove_user_favorite_product'),
    # path('change_user_favorite_product_count/',views.change_user_favorite_product_count,name='change_user_favorite_product_count'),
    
]
