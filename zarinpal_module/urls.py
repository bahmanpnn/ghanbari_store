from django.urls import path
from . import views

app_name="zarinpal_module"
urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify_payment , name='verify'),
]