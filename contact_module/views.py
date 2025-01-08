from django.shortcuts import render
from django.views import View
from .forms import ContactForm


class ContactUsView(View):
    template_name="contact_module/contact_us.html"
    form_class=ContactForm

    def get(self,request):
        return render(request,self.template_name,{
            'form':self.form_class()
        })
    