from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from blog_module.models import Article
from product_module.models import Product
from django.template.loader import render_to_string
from .models import Slider
from site_settings_module.models import SiteSetting,FooterLinkBox
from contact_module.forms import NewsEmailForm
from django.contrib import messages


class homePageView(View):
    def get(self,request):
        latest_articles=Article.objects.filter(is_active=True).order_by('-created_date')[:4]
        latest_discounted_products=Product.objects.filter(is_active=True,discount_percent__gte=1).prefetch_related('images').order_by('-added_date')[:10]
        
        return render(request,'home_module/home.html',{
            'latest_articles':latest_articles,
            'latest_discounted_products':latest_discounted_products
        })
    

def header_component(request):
    return render(request,'header_component.html')

def mobile_sidebar_component(request):
    return render(request,'mobile_sidebar_component.html')

def navbar_component(request):
    return render(request,'navbar_component.html')

def slider_component(request):
    sliders=Slider.objects.filter(is_active=True)
    
    return render(request,'home_module/includes/slider_component.html',{
        'sliders':sliders
    })


class FooterEmailSubmitView(View):
    form_class = NewsEmailForm

    def post(self, request):
        email_form = self.form_class(request.POST)
        if email_form.is_valid():
            email_form.save()
            # Redirect back to the page the user came from
            messages.success(request, "ایمیل شما با موفقیت ثبت شد.")
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to referrer or home if referrer is not available
        else:
            messages.warning(request, "مشکلی در ثبت ایمیل شما پیش اومده. لطفاً دوباره تلاش کنید.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

            # latest_articles=Article.objects.filter(is_active=True).order_by('-created_date')[:4]
            # latest_discounted_products=Product.objects.filter(is_active=True,discount_percent__gte=1).prefetch_related('images').order_by('-added_date')[:10]
            # try:
            #     site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
            # except:
            #     site_setting = None
            # footer_link_boxes = FooterLinkBox.objects.all()
            
            # return render(request,'home_module/home.html',{
            #     'latest_articles':latest_articles,
            #     'latest_discounted_products':latest_discounted_products,
            #     'site_setting': site_setting,
            #     'footer_link_boxes': footer_link_boxes,
            #     'email_form': self.form_class(request.POST)
            # })


class FooterComponent(View):
    form_class = NewsEmailForm
    def get(self, request):
        try:
            site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        except:
            site_setting = None
        footer_link_boxes = FooterLinkBox.objects.all()

        return render(request, "footer_component.html", {
            'site_setting': site_setting,
            'footer_link_boxes': footer_link_boxes,
            'email_form': self.form_class()
        })


def copyright_component(request):
    return render(request,'copyright_component.html')
