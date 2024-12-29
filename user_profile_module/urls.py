from django.urls import path
from . import views


app_name="user_profile_module"
urlpatterns = [
    path('',views.UserProfileView.as_view(),name='user-profile'),
]
