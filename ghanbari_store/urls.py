from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home_module.urls',namespace='home_module')),
    path('account/',include('account_module.urls',namespace='account_module')),
    path('contact-us/',include('contact_module.urls',namespace='contact_module')),
    path('about-us/',include('about_us_module.urls',namespace='about_us_module')),
    path('products/',include('product_module.urls',namespace='product_module')),
    path('orders/',include('order_module.urls',namespace='order_module')),
    path('articles/',include('blog_module.urls',namespace='blog_module')),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
