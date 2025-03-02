from django.urls import reverse
import requests
import json
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from order_module.models import OrderBasket
from order_module.forms import CheckOutForm
from site_settings_module.models import SiteSetting
from order_module.models import Checkout

# Determine sandbox or live API
sandbox = "sandbox" if settings.ZARINPAL_SANDBOX else "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

@login_required(login_url='login-page')
def send_request(request):
    if request.method != "POST":
        return redirect("order_module:order-basket")
    
    user = request.user
    address = user.user_address.first() 
    user_basket=OrderBasket.objects.prefetch_related('order_detail').filter(is_paid=False, user_id=request.user.id).first()
    
    if not user_basket:
        return JsonResponse({"status": False, "error": "No unpaid order found"})
    
    if not user_basket.order_detail.all().exists():
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect("order_module:order-basket")


    # form = CheckOutForm(request.POST, instance=address, user=user)

    # Fetch existing checkout instance (if any)
    checkout_instance, created = Checkout.objects.get_or_create(order_basket=user_basket, defaults={'user': user})

    # Bind form with data and existing instance
    form = CheckOutForm(request.POST, user=user, checkout_instance=checkout_instance)

    if form.is_valid():
        # Update existing checkout instance instead of creating a new one
        for field, value in form.cleaned_data.items():
            setattr(checkout_instance, field, value)

        # Ensure user and order_basket are always set
        checkout_instance.user = user
        checkout_instance.order_basket = user_basket

        checkout_instance.save()  # Save changes

    else:
        context={
            'form':form,
            'order_basket':user_basket,
            'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
            'transportation_rate': SiteSetting.get_transportation_rate(),
            'total':user_basket.get_total_amount() if user_basket.get_total_amount() > SiteSetting.get_free_shipping_threshold() else SiteSetting.get_free_shipping_threshold()+user_basket.get_total_amount(),
        }
        return render(request,"order_module/checkout.html",context)

    pay_amount=user_basket.get_total_amount()
    if pay_amount <=SiteSetting.get_free_shipping_threshold():
        # add transportation rate to pay amount
        pay_amount+=SiteSetting.get_transportation_rate()
    
    
    """Handles sending a payment request to ZarinPal."""
    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": pay_amount*10,  # Rial / Required
        "callback_url": settings.ZARINPAL_CALLBACK_URL,
        "description": "نهایی کردن سفارش",
        "metadata": {"mobile": user.phone_number, "email": user.email if user.email else ""}
    }

    headers = {"accept": "application/json", "content-type": "application/json"}

    try:
        cache.set(f"user_basket_id:{user.phone_number}", user_basket.id, timeout=600)
    except Exception as e:
        print(f"Redis error: {e}") 

    try:
        response = requests.post(ZP_API_REQUEST, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("data") and result["data"].get("code") == 100:
                authority = result["data"]["authority"]
                payment_url = f"{ZP_API_STARTPAY}{authority}"
                return redirect(payment_url)
                # return JsonResponse({"status": True, "url": payment_url, "authority": authority})
            else:
                return JsonResponse({"status": False, "error": result.get("errors")})
        
        return JsonResponse({"status": False, "error": "Invalid response from ZarinPal"})

    except requests.exceptions.Timeout:
        return JsonResponse({"status": False, "error": "Request timed out"})
    except requests.exceptions.ConnectionError:
        return JsonResponse({"status": False, "error": "Connection error"})
    

@login_required(login_url='login-page')
def verify_payment(request):
    user=request.user
    user_basket_id = cache.get(f"user_basket_id:{user.phone_number}")
    if not user_basket_id:
        return JsonResponse({"status": False, "error": "Payment session expired, please retry."})


    user_basket=OrderBasket.objects.prefetch_related('order_detail').filter(id=user_basket_id,is_paid=False,user_id=request.user.id).first()
    if user_basket is None:
        return JsonResponse({"status": False, "error": "No unpaid order found"})
    
    pay_amount=user_basket.get_total_amount()
    if pay_amount <=SiteSetting.get_free_shipping_threshold():
        # add transportation rate to pay amount
        pay_amount+=SiteSetting.get_transportation_rate()


    """Handles ZarinPal payment verification."""
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    if not authority or status != "OK":
        # return JsonResponse({"status": False, "error": "Payment failed or was canceled by the user"})
        messages.error(request,'پرداخت شما با خطا مواجه شد.اگر پرداخت از سمت شما لغو نشده است لطفا مجدد تلاش نمایید')
        return redirect(reverse("home_module:home-page"))


    verify_data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": pay_amount*10,  # Must match the original request
        "authority": authority
    }

    headers = {"accept": "application/json", "content-type": "application/json"}

    try:
        response = requests.post(f"{ZP_API_VERIFY}", 
                                 json=verify_data, headers=headers, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get("data") and result["data"].get("code") == 100:
                user_basket.is_paid=True
                user_basket.payment_date=now()

                # set final price for order details
                for order_detail in user_basket.order_detail.all():
                    order_detail.final_price = order_detail.product.price_with_discount or order_detail.product.price
                    order_detail.save()
                
                user_basket.save()



                checkout_instance = Checkout.objects.filter(order_basket=user_basket).first()
                if checkout_instance:
                    checkout_instance.is_successfull = True
                    checkout_instance.save()

                # user_basket.checkout.is_successfull = True
                # user_basket.checkout.save()

                cache.delete(f"user_basket_id:{user.phone_number}")
                # print('user paid successfully')
                # return JsonResponse({"status": True, "ref_id": result["data"]["ref_id"]})
                messages.success(request,"خرید شما با موفیقت ثبت شد.پس از بررسی های لازم بسته شما ارسال خواهد شد")
                return redirect(reverse("home_module:home-page"))
            else:
                return JsonResponse({"status": False, "error": result.get("errors")})
        
        return JsonResponse({"status": False, "error": "Invalid response from ZarinPal"})

    except requests.exceptions.Timeout:
        print(requests.exceptions)
        return JsonResponse({"status": False, "error": "Request timed out"})
    except requests.exceptions.ConnectionError:
        return JsonResponse({"status": False, "error": "Connection error"})



