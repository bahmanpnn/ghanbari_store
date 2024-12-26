from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from blog_module.models import Article
from product_module.models import Product
from django.template.loader import render_to_string


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
    return render(request,'home_module/includes/slider_component.html')

def footer_component(request):
    return render(request,'footer_component.html')

def copyright_component(request):
    return render(request,'copyright_component.html')

def change_modal_data(request):
    product_id=request.GET.get('product_id')

    target_product=get_object_or_404(Product,id=product_id)
    context={
        'product':target_product
    }
    return JsonResponse({
        'status':'success',
        'body':render_to_string("home_module/includes/product_modal.html",context)
    })