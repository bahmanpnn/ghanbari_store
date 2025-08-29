from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView,DetailView, FormView
from django.db.models import Sum,Count
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from user_profile_module.models import UserFavoriteProduct
from account_module.models import User
from .models import Product,ProductImage, ProductCommentReview
from .forms import ProductFilterForm,ProductCommentReviewForm
from .models import Product, ProductCommentReview


class ProductListView(ListView):
    template_name="product_module/products.html"
    model=Product
    context_object_name='products'
    ordering=['-added_date']
    paginate_by=5


    def get_queryset(self):        
        query=super().get_queryset().filter(is_active=True)

        search_query = self.request.GET.get('product-search', '')
        product_filter = self.request.GET.get('product_filter')

        if search_query:
            query = query.filter(
                Q(title__icontains=search_query) |  # Search in title
                Q(short_description__icontains=search_query)  # Search in short_description
            )

        if product_filter == "discounted":
            query=query.filter(discount_percent__gte=1)

        elif product_filter == "no-discount":
            query=query.filter(discount_percent__lte=0)
            # query=query.filter(product__discount_percent__gte=1,is_active=True)

        elif product_filter == "most-bought":
            # query = query.annotate(buy_count=Count('orderitem')).order_by('-buy_count')
            query = query.annotate(
                total_sold=Sum('orderdetail__count', filter=Q(orderdetail__order_basket__is_paid=True))
            ).order_by('-total_sold')


        return query
    
    def get_context_data(self, **kwargs):
        '''
            if need to pass new data in product template and
            this is not product model must send with this method and override this
        '''
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['filter_form']=ProductFilterForm(self.request.GET or None)
        return context
    

class ProductDetailView(DetailView,FormView):
    template_name='product_module/product_detail.html'
    model=Product
    context_object_name='product'
    form_class=ProductCommentReviewForm

    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product=self.object
        
        # product images
        product_images=list(ProductImage.objects.filter(product_id=loaded_product.id).all())
        product_images.insert(0,loaded_product)
        context['product_images']=product_images

        # accepted product comments
        # context['avg_rate']=loaded_product.avg_rate,  # Pass average rating
        accepted_comments = ProductCommentReview.objects.filter(product=loaded_product, status=2).order_by('-created_date')
        context.update({
            "accepted_comments": accepted_comments,
            "avg_rate": loaded_product.avg_rate,
            # "form": self.form_class(),
            "form": self.get_form(),
        })

        return context
    
    def get_object(self, queryset = None):
        queryset=Product.objects.get(pk=self.kwargs['pk'],slug=self.kwargs['slug'])
        return queryset 

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user  # Pass the logged-in user to the form
    #     return kwargs
    
    # def form_valid(self, form):
    #     product = self.get_object()
    #     comment = form.save(commit=False)
    #     comment.product = product
    #     comment.user = self.request.user  # Assuming the user is logged in
    #     comment.save()
    #     return super().form_valid(form)
    
    # def get_success_url(self):
    #     return self.get_object().get_absolute_url()  # Reload product page

    # def get_success_url(self):
    #     return self.request.path  # Redirect to the same product detail page after form submission

    

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     """Handle form submission."""
    #     self.object = self.get_object()  # Load product instance
    #     form = self.get_form()

    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


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


def add_product_comment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            comment_text = request.POST.get('comment')
            product_rating = request.POST.get('product_rating')

            # Check if product exists
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'status': 'invalid-product',
                                     'icon':'error',
                                     'title':'خطا',
                                        'message': 'محصول پیدا نشد'})
            
            user=request.user.id
            check_user=User.objects.get(id=user)
            if not check_user:
                return JsonResponse({'status': 'user-not-found',
                                     'icon':'error',
                                     'title':'خطا',
                                        'message': 'حساب کاربری پیدا نشد'})
            
            # Create and save comment (assuming you have a user system)
            ProductCommentReview.objects.create(
                product_id=product_id,
                user=request.user,  # Assuming the user is authenticated
                description=comment_text,
                rating=product_rating,
                status="0"  # Assuming "0" means pending review
            )

            return JsonResponse({'status': 'success',
                                 'icon':'success',
                                  'message': 'نظر شما با موفقیت ثبت شد.پس از بررسی ادمین نظر شما به نظرات اضافه میشود'})

        return JsonResponse({'status': 'not-authenticated',
                             'icon':'warning',
                             'title':'هشدار',
                              'message': 'کاربر احراز هویت لازم دارد!'})
    return JsonResponse({'status': 'error',
                         'icon':'error',
                         'title':'خطا',
                          'message': 'درخواست نامعتبر!!'})



# class ProductDetailView(DetailView):
#     template_name='product_module/product_detail.html'
#     model=Product
#     context_object_name='product'
    
#     def get_queryset(self):
#         return super().get_queryset()
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         loaded_product=self.object
#         product_images=list(ProductImage.objects.filter(product_id=loaded_product.id).all())
#         product_images.insert(0,loaded_product)
#         context['product_images']=product_images
#         return context

#     def get_object(self, queryset = None):
#         queryset=Product.objects.get(pk=self.kwargs['pk'],slug=self.kwargs['slug'])
#         return queryset 
