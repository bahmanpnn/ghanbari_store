from django.urls import path
from . import views


app_name='home_module'
urlpatterns = [
    path('',views.homePageView.as_view(),name='home-page'),    
    path('change-modal-data/',views.change_modal_data,name='change-modal-data'),    
]
