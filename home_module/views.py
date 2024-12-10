from django.shortcuts import render
from django.views import View


class homePageView(View):
    def get(self,request):
        return render(request,'home_module/home.html')
    

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