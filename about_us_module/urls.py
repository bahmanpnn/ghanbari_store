from django.urls import path
from . import views


app_name='about_us_module'
urlpatterns = [
    path('about-us/',views.AboutUsView.as_view(),name='about-us'),
]
