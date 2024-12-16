import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse,HttpResponse
from django.shortcuts import redirect, render
# from django.urls import reverse
from django.views import View
# from django.template.loader import render_to_string
# from django.contrib import messages
# from permissions import is_authenticated_permission
from product_module.models import Product
from .models import OrderBasket,OrderDetail
# from .forms import CouponApplyForm
# from .models import Coupon


# Done
def add_product_to_basket(request):
    if request.user.is_authenticated:
        
        product_id=int(request.GET.get('product_id'))
        count=int(request.GET.get('count')) #get method returns str
        if count<=0:
            return JsonResponse({
            'status':'not-invalid',
            'title':'alert',
            'text':'اطلاعات نامعتبر',
            'icon':'error',
            'confirm_button_text':'باشه'
        })

        product=Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()

        if product is not None:
            current_order,is_created=OrderBasket.objects.get_or_create(is_paid=False,user_id=request.user.id)
            current_order_detail=current_order.order_detail.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count+=count
                current_order_detail.save()
            else:
                new_order_detail=OrderDetail(product_id=product_id,count=count,order_basket_id=current_order.id)
                new_order_detail.save()
                
            return JsonResponse({
                'status':'success',
                'title':'اعلان',
                'text':'محصول به سبد خرید شما با موفقیت اضافه شد',
                'icon':'success',
                'confirm_button_text':'باشه'
            })
        else:
            return JsonResponse({
                'status':'not-invalid',
                'title':'alert',
                'text':'اطلاعات نامعتبر',
                'icon':'error',
                'confirm_button_text':'باشه'
            })
    else:
        return JsonResponse({
            'status':'not-authenticated',
            'title':'هشدار',
            'text':'ابتدا باید وارد حساب خود شوید',
            'icon':'warning',
            'confirm_button_text':'رفتن به صفحه ورود'
        })


class UserOrderBasket(View,LoginRequiredMixin):
    template_name='order_module/basket.html'

    def get(self,request):
        current_basket,is_created=OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False,user_id=request.user.id)

        return render(request,self.template_name,{
            'basket':current_basket,
            # 'total_price':current_basket.get_total_amount,
            })
    
    