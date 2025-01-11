from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from .forms import ContactForm
from django.contrib import messages
from site_settings_module.models import SiteSetting


class ContactUsView(View):
    template_name="contact_module/contact_us.html"
    form_class=ContactForm
    try:
        main_site_setting=SiteSetting.objects.filter(is_main_setting=True).first()
    except:
        main_site_setting=None

    def get(self,request):
        return render(request,self.template_name,{
            'form':self.form_class(),
            'main_site_setting':self.main_site_setting
        })
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'پیام شما با موفقیت ارسال شد')
            return redirect(reverse("contact_module:contact-us"))
        return render(request,self.template_name,{
            'form':self.form_class(request.POST),
            'main_site_setting':self.main_site_setting
        })