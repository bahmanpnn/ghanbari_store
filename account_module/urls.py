from django.urls import path
from . import views


app_name='account_module'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user-register'),    
]
