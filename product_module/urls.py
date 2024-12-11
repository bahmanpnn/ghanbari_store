from django.urls import path
from . import views


app_name="product_module"
urlpatterns = [
    path('top-filter/',views.ProductListView.as_view(),name='products'),
    path('sidbar-filter/',views.ProductTwoListView.as_view(),name='products-two'),
]
