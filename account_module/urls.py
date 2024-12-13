from django.urls import path
from . import views


app_name='account_module'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user-register'),    
    path('login/',views.UserLoginView.as_view(),name='user-login'),    
    path('logout/',views.UserLogOutView.as_view(),name='user-logout'),    
]
