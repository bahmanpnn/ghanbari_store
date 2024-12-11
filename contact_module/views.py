from django.shortcuts import render
from django.views import View


class ContactUsView(View):
    template_name="contact_module/contact_us.html"

    def get(self,request):
        return render(request,self.template_name)
    