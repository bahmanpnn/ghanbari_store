from django.urls import path
from . import views


app_name='contact_module'
urlpatterns = [
    path('contact-us/',views.ContactUsView.as_view(),name="contact-us"),
]
