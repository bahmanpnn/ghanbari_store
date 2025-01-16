from django.urls import path,re_path
from . import views


app_name="product_module"
urlpatterns = [
    # products 
    path('',views.ProductListView.as_view(),name='products'),
    # product detail
    path('<int:pk>/<slug:slug>/',views.ProductDetailView.as_view(),name='product-detail'),
    re_path(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/\Z$', views.ProductDetailView.as_view(), name='product-detail'),
    # add product to user fav list
    path('add-to-user-favorite-list/',views.add_remove_product_to_favorite_list,name='add-product-to-favorite-list'),
]
