from django.shortcuts import render
from django.views import View


class ProductListView(View):
    template_name="product_module/products.html"
    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):
        pass

class ProductTwoListView(View):
    template_name="product_module/products2.html"
    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):
        pass