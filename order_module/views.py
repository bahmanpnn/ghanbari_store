# import datetime
# from django.urls import reverse
# from django.template.loader import render_to_string
# from django.contrib import messages
# from permissions import is_authenticated_permission
# from .forms import CouponApplyForm
# from .models import Coupon
# from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse,HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from product_module.models import Product
from site_settings_module.models import SiteSetting
from .models import OrderBasket,OrderDetail,Coupon
from .forms import CheckOutForm
from django.contrib import messages



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
        current_basket, _ = OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False, user_id=request.user.id)

        return render(request, self.template_name, {
            'user_basket': current_basket,
            'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
            'transportation_rate': SiteSetting.get_transportation_rate(),
        })

    
@login_required
def remove_user_basket_card_order_detail(request):
    detail_id = request.GET.get('detail_id')

    current_basket = OrderBasket.objects.prefetch_related('order_detail').filter(is_paid=False, user_id=request.user.id).first()
    # current_basket, _ = OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False, user_id=request.user.id)
    
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
        
        # updated_basket = OrderBasket.objects.prefetch_related('order_detail').filter(is_paid=False, user_id=request.user.id).first()
        # updated_basket, _ = OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False, user_id=request.user.id)
        current_basket.order_detail.set(current_basket.order_detail.exclude(id=detail_id))

    context = {
        'user_basket': current_basket,
        'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
        'transportation_rate': SiteSetting.get_transportation_rate(),
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

    current_basket, _ = OrderBasket.objects.prefetch_related('order_detail').get_or_create(is_paid=False, user_id=request.user.id)

    context = {
        'user_basket': current_basket,
        'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
        'transportation_rate': SiteSetting.get_transportation_rate(),
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string("order_module/includes/remove_order_detail_ajax.html", context)
    })


@csrf_exempt
def apply_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code", "").strip()

        if not coupon_code:
            return JsonResponse({"status": "error", "message": "کد تخفیف را وارد کنید!"})

        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({"status": "error", "message": "کد تخفیف نامعتبر است!"})

        if not coupon.is_valid():
            return JsonResponse({"status": "error", "message": "کد تخفیف منقضی شده است!"})

        # Get the user's basket
        basket = OrderBasket.objects.prefetch_related('order_detail').filter(user=request.user, is_paid=False).first()

        if not basket:
            return JsonResponse({"status": "error", "message": "سبد خریدی یافت نشد!"})

        # Apply coupon
        if basket.coupon and basket.coupon == coupon:
            return JsonResponse({"status": "error", "message": "کد تخفیف قبلا اعمال شده"})
        basket.coupon = coupon
        basket.save(update_fields=["coupon"])

        total_with_tr=float(basket.get_total_amount())+float(SiteSetting.get_transportation_rate())

        context = {
            'user_basket': basket,
            'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
            'transportation_rate': SiteSetting.get_transportation_rate(),
            'total_with_tr':total_with_tr
            }

        return JsonResponse({
            "status": "success",
            "message": "کد تخفیف اعمال شد!",
            'body': render_to_string("order_module/includes/remove_order_detail_ajax.html", context),
            "new_total": basket.get_total_amount(),
        })

    return JsonResponse({"status": "error", "message": "درخواست نامعتبر است!"})


class CheckOutView(View,LoginRequiredMixin):
    template_name="order_module/checkout.html"
    form_class=CheckOutForm

    def get(self,request):
        user = request.user
        address = user.user_address.first()  # Get the first address if available
        user_order_basket=OrderBasket.objects.prefetch_related('order_detail').filter(is_paid=False, user_id=request.user.id).first()

        context={
            'form':self.form_class(instance=address, user=user),
            'order_basket':user_order_basket,
            'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
            'transportation_rate': SiteSetting.get_transportation_rate(),
            'total':user_order_basket.get_total_amount() if user_order_basket.get_total_amount() > SiteSetting.get_free_shipping_threshold() else SiteSetting.get_free_shipping_threshold()+user_order_basket.get_total_amount(),
        }
        return render(request,self.template_name,context)

    # def post(self,request):
    #     user = request.user
    #     address = user.user_address.first() 
    #     user_order_basket=OrderBasket.objects.prefetch_related('order_detail').filter(is_paid=False, user_id=request.user.id).first()
    #     if not user_order_basket.order_detail:
    #         messages.error(request, "سبد خرید شما خالی است.")
    #         return redirect("order_module:order-basket")

    #     form = CheckOutForm(request.POST, instance=address, user=user)
    #     if form.is_valid():
    #         # Save user address (update existing or create new)
    #         user_address = form.save(commit=False)
    #         user_address.user = user
    #         user_address.save()
            
    #         # Proceed to payment
    #         return redirect("zarinpal_module:request")
        

    #     context={
    #         'form':self.form_class(instance=address, user=user),
    #         'order_basket':user_order_basket,
    #         'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
    #         'transportation_rate': SiteSetting.get_transportation_rate(),
    #         'total':user_order_basket.get_total_amount() if user_order_basket.get_total_amount() > SiteSetting.get_free_shipping_threshold() else SiteSetting.get_free_shipping_threshold()+user_order_basket.get_total_amount(),
    #     }
    #     return render(request,self.template_name,context)
    





# from django.shortcuts import redirect, get_object_or_404
# from django.utils.timezone import now
# from .models import OrderBasket, Checkout
# from payment_gateway import process_payment  # Hypothetical function


# def checkout(request):
#     user = request.user
#     order_basket = get_object_or_404(OrderBasket, user=user, is_paid=False)

#     # Create a new checkout instance (even if user retries payment)
#     checkout_instance = Checkout.objects.create(
#         user=user,
#         order_basket=order_basket,
#         phone_number=user.phone_number,
#         email=user.email,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         province=user.user_address.first().province if user.user_address.exists() else "",
#         city=user.user_address.first().city if user.user_address.exists() else "",
#         main_address=user.user_address.first().main_address if user.user_address.exists() else "",
#         zip_code="",
#         about_order_text=request.POST.get("about_order_text", ""),
#         is_successful=False,  # Payment pending
#     )

#     # Redirect to payment gateway
#     payment_response = process_payment(order_basket)

#     if payment_response.get("status") == "success":
#         # Payment was successful → Update Checkout
#         checkout_instance.is_successful = True
#         checkout_instance.save(update_fields=["is_successful"])

#         # Mark order as paid
#         order_basket.is_paid = True
#         order_basket.payment_date = now()
#         order_basket.save(update_fields=["is_paid", "payment_date"])

#         # Delete old unsuccessful checkouts
#         Checkout.objects.filter(user=user, order_basket=order_basket, is_successful=False).delete()

#         return redirect("payment_success_url")

#     return redirect("payment_failed_url")


















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
