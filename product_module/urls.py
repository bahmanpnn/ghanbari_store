from django.urls import path,re_path
from . import views


app_name="product_module"
urlpatterns = [
    path('top-filter/',views.ProductListView.as_view(),name='products'),

    path('<int:pk>/<slug:slug>/',views.ProductDetailView.as_view(),name='product-detail'),
    re_path(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/\Z$', views.ProductDetailView.as_view(), name='product-detail'),
    
    
    
]
