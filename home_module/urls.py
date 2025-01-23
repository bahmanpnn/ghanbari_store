from django.urls import path
from . import views


app_name='home_module'
urlpatterns = [
    path('',views.homePageView.as_view(),name='home-page'),
    path('footer_component/',views.FooterEmailSubmitView.as_view(),name='footer-component'),

]
