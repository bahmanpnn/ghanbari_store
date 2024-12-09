from django.shortcuts import render
from django.views import View


class homePageView(View):
    def get(self,request):
        return render(request,'home_module/home.html')
    

def header_component(request):
    return render(request,'header_component.html')

def footer_component(request):
    return render(request,'footer_component.html')