from datetime import datetime, timedelta
from django.utils.timezone import now
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Sum,Count
from product_module.models import Product
from site_settings_module.models import SiteSetting,FooterLinkBox
from contact_module.forms import NewsEmailForm
from blog_module.models import Article
from product_module.models import ProductOfTheWeek
from .models import Slider


class homePageView(View):
    def get(self,request):
        latest_articles=Article.objects.filter(is_active=True).order_by('-created_date')[:4]

        product_of_the_week = ProductOfTheWeek.objects.filter(start_date__lte=datetime.now(),end_date__gte=datetime.now(),is_active_bool=True).first()
        # product_of_the_week = ProductOfTheWeek.objects.filter(start_date__lte=now(),end_date__gte=now(),is_active_bool=True).first()
        most_bought_products=Product.objects.annotate(buy_count=Sum('orderdetail__count')).filter(is_active=True,is_delete=False,orderdetail__order_basket__is_paid=True).order_by('-buy_count')[:2]
        if product_of_the_week:
            most_bought_products=most_bought_products[:1]

        # Fetch 4 random products excluding "Product of the Week" and "Most Bought Products"
        excluded_ids = list(most_bought_products.values_list('id', flat=True))
        if product_of_the_week:
            excluded_ids.append(product_of_the_week.product.id)
        
        other_products = Product.objects.filter(
            is_active=True,
            is_delete=False
        ).exclude(id__in=excluded_ids)[:4]

        # Randomize and limit to 4 products
        # other_products = list(other_products)
        # random.shuffle(other_products)

        return render(request,'home_module/home.html',{
            'latest_articles':latest_articles,
            'product_of_the_week':product_of_the_week,
            'most_bought_products':most_bought_products,
            'other_products':other_products
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
