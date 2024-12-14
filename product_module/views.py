from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Product


class ProductListView(ListView):
    template_name="product_module/products.html"
    model=Product
    context_object_name='products'
    ordering=['-added_date']
    paginate_by=5


    def get_queryset(self):        
        query=super().get_queryset().filter(is_active=True)
        
        # if self.kwargs:
        #     category=self.kwargs.get('category')
        #     if category is not None:
        #         query=query.filter(category__url_title__iexact=category,is_active=True)

        return query
    
    def get_context_data(self, **kwargs):
        '''
            if need to pass new data in product template and
            this is not product model must send with this method and override this
        '''
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context
    
    def post(self,request):
        pass
    

class ProductTwoListView(View):
    template_name="product_module/products2.html"
    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):
        pass