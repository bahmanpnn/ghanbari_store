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
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from site_settings_module.models import SiteSetting


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


@method_decorator(login_required, name='dispatch')
class UserOrderBasket(View, LoginRequiredMixin):
    template_name = 'order_module/basket.html'

    def get(self, request):
        current_basket, _ = OrderBasket.objects.get_or_create(is_paid=False, user_id=request.user.id)

        return render(request, self.template_name, {
            'user_basket': current_basket,
            'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
        })

    
@login_required
def remove_user_basket_card_order_detail(request):
    detail_id = request.GET.get('detail_id')
    current_basket, _ = OrderBasket.objects.get_or_create(is_paid=False, user_id=request.user.id)

    if detail_id == "all":
        current_basket.order_detail.all().delete()
    elif detail_id is None:
        return JsonResponse({'status': 'detail-not-found'})
    else:
        count, _ = OrderDetail.objects.filter(
            id=detail_id, order_basket=current_basket
        ).delete()
        
        if count == 0:
            return JsonResponse({'status': 'detail-not-found'})

    context = {
        'user_basket': current_basket,
        'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string("order_module/includes/basket_cart.html", context),
        'mbody': render_to_string("order_module/includes/remove_order_detail_ajax.html", context)
    })


@login_required
def change_order_detail_count(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if not detail_id or not state:
        return JsonResponse({'status': 'invalid-request'})

    target_order_detail = OrderDetail.objects.filter(
        order_basket__user_id=request.user.id, id=detail_id, order_basket__is_paid=False
    ).first()

    if not target_order_detail:
        return JsonResponse({'status': 'detail-not-found'})

    if state == "increase":
        target_order_detail.count += 1
        target_order_detail.save()
    elif state == "decrease":
        if target_order_detail.count == 1:
            target_order_detail.delete()
        else:
            target_order_detail.count -= 1
            target_order_detail.save()
    else:
        return JsonResponse({'status': 'invalid-state'})

    current_basket, _ = OrderBasket.objects.get_or_create(is_paid=False, user_id=request.user.id)

    context = {
        'user_basket': current_basket,
        'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string("order_module/includes/remove_order_detail_ajax.html", context)
    })
















# @method_decorator(login_required,name='dispatch')
# class UserOrderBasket(View,LoginRequiredMixin):
#     template_name='order_module/basket.html'

#     def get(self,request):
#         current_basket,_=OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False,user_id=request.user.id)
#         need_for_free_transportation=SiteSetting.get_free_shipping_threshold()

#         return render(request,self.template_name,{
#             'user_basket':current_basket,
#             'need_for_free_transportation':need_for_free_transportation,
#             })



# @login_required
# def remove_user_basket_card_order_detail(request):
#     detail_id=request.GET.get('detail_id')
#     need_for_free_transportation=SiteSetting.get_free_shipping_threshold()
#     if detail_id == "all":
#         current_basket,_=OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False,user_id=request.user.id)
#         current_basket.order_detail.all().delete()
        

#         context={
#             'user_basket':current_basket,
#             'need_for_free_transportation':need_for_free_transportation,
#             }
#         return JsonResponse({
#             'status':'success',
#             'body':render_to_string("order_module/includes/basket_cart.html",context),
#             'mbody':render_to_string("order_module/includes/remove_order_detail_ajax.html",context)
#         })

#     elif detail_id is None:
#         return JsonResponse({
#             'status':'detail-not-found'
#         })

#     count,target_order_detail=OrderDetail.objects.filter(id=detail_id,order_basket__is_paid=False,order_basket__user_id=request.user.id).delete()
#     if count == 0:
#         return JsonResponse({
#             'status':'detail_not_found'
#         })
    
#     current_basket,_=OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False,user_id=request.user.id)

#     # total=total_price+tax    
#     context={
#         'user_basket':current_basket,
#         'need_for_free_transportation':need_for_free_transportation,
#         }

#     return JsonResponse({
#         'status':'success',
#         'body':render_to_string("order_module/includes/basket_cart.html",context),
#         'mbody':render_to_string("order_module/includes/remove_order_detail_ajax.html",context)
#     })


# @login_required
# def change_order_detail_count(request):
#     detail_id=request.GET.get('detail_id')
#     state=request.GET.get('state')

#     if detail_id is None or state is None:
#         return JsonResponse({
#             'status':'invalid-request'
#         })

#     target_order_detail=OrderDetail.objects.filter(order_basket__user_id=request.user.id,id=detail_id,order_basket__is_paid=False).first()
#     if target_order_detail is None:
#         return JsonResponse({
#             'status':'detail-not-found'
#         })
    
#     if state == "increase":
#         target_order_detail.count+=1
#         target_order_detail.save()
#     elif state == "decrease" and target_order_detail.count ==1:
#         target_order_detail.delete()
#     elif state == "decrease" and target_order_detail.count >=1:
#         target_order_detail.count-=1
#         target_order_detail.save()
#     else:
#         return JsonResponse({
#             'status':'invalid state'
#         })
    
#     current_basket,is_created=OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False,user_id=request.user.id)
#     need_for_free_transportation=SiteSetting.get_free_shipping_threshold()
#     # total_price=current_basket.get_total_amount()
#     # tax=total_price/10
#     # total=total_price+tax 
#     context={
#         'user_basket':current_basket,
#         'need_for_free_transportation':need_for_free_transportation,
#         }

#     return JsonResponse({
#         'status':'success',
#         'body':render_to_string("order_module/includes/remove_order_detail_ajax.html",context)
#     })
