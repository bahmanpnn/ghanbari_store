from django.urls import path
from . import views


app_name='account_module'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user-register'),    
    path('login/',views.UserLoginView.as_view(),name='user-login'),    
    path('forget-password/',views.UserForgetPasswordView.as_view(),name='user-forget-password'),    
    path('change-password/',views.UserChangePasswordView.as_view(),name='user-change-password'),    
    path('otp-code/',views.UserOtpCode.as_view(),name='user-otp-code'),    
    path('logout/',views.UserLogOutView.as_view(),name='user-logout'),    
]
