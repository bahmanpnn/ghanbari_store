from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView,DetailView
from .models import Product
from user_profile_module.models import UserFavoriteProduct
from django.http import JsonResponse


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


class ProductDetailView(DetailView):
    template_name='product_module/product_detail.html'
    model=Product
    context_object_name='product'
    
    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset = None):
        queryset=Product.objects.get(pk=self.kwargs['pk'],slug=self.kwargs['slug'])
        return queryset 


def add_remove_product_to_favorite_list(request):
    if request.user.is_authenticated:
        product_id=int(request.GET.get('product_id'))
        target_product=get_object_or_404(Product,id=product_id,is_active=True,is_delete=False)
        if target_product is not None:
            check_product=UserFavoriteProduct.objects.filter(product_id=product_id,user_id=request.user.id).first()
            if check_product is not None:
                check_product.delete()
                return JsonResponse({
                        'status':'success',
                        'title':'هشدار',
                        'text':'از لیست مورد علاقه ها حذف شد',
                        'icon':'success',
                        'confirm_button_text':'باشه',
                        'product_id':product_id,
                        'action':'removing'
                    })
            else:    
                add_product_to_favorites=UserFavoriteProduct(user_id=request.user.id,product_id=target_product.id)
                add_product_to_favorites.save()

                return JsonResponse({
                        'status':'success',
                        'title':'هشدار',
                        'text':'به لیست مورد علاقه ها اضافه شد',
                        'icon':'success',
                        'confirm_button_text':'باشه',
                        'product_id':product_id,
                        'action':'adding'
                    })
        
        else:
            return JsonResponse({
                'status':'invalid-product-id',
                'title':'خطا',
                'text':'اطلاعات نامعتبر',
                'icon':'error',
                'confirm_button_text':'باشه'
            })
    else:
        return JsonResponse({
            'status':'not-authenticated',
            'title':'هشدار',
            'text':'برای اضافه کردن محصول به لیست مورد علاقه های خود باتدا باید وارد حساب کاربری خود شوید',
            'icon':'error',
            'confirm_button_text':'ورود به حساب'
            })
    