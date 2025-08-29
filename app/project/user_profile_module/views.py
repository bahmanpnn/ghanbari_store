from django.shortcuts import redirect, render
from django.http import JsonResponse,HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import login,logout
from django.template.loader import render_to_string
from account_module.models import User,UserAddress
from order_module.models import OrderBasket
from .forms import EditUserAddressForm,EditUserInformationForm,ChangePasswordForm
from .models import UserFavoriteProduct
# from permissions import is_authenticated_permission
# from django.utils.decorators import method_decorator
from site_settings_module.models import SiteBanner



# @method_decorator(is_authenticated_permission,name='dispatch')
class UserProfileView(View):
    template_name = 'user_profile_module/user_profile.html'
    address_form = EditUserAddressForm
    user_information_form = EditUserInformationForm
    user_password_form = ChangePasswordForm

    def get(self, request):
        user_orders = OrderBasket.objects.annotate(items=Count('order_detail')).filter(is_paid=True, user_id=request.user.id).order_by('-payment_date')
        user_address = UserAddress.objects.filter(user=request.user).first()
        profile_dashboard_banner=SiteBanner.objects.filter(is_active=True,position__exact=SiteBanner.SiteBannerPosition.profile_dashboard).first()
        

        return render(request, self.template_name, {
            'user_orders': user_orders,
            'address_form': self.address_form(instance=user_address),
            'user_information_form': self.user_information_form(instance=request.user),
            'user_password_form': self.user_password_form(),
            'profile_dashboard_banner':profile_dashboard_banner
        })

    def post(self, request):
        if 'user-address' in request.POST:
            # for new user that has no useraddress it is None and it set for instance.
            user_address = UserAddress.objects.filter(user=request.user).first() 
            address_form = self.address_form(request.POST, instance=user_address)

            if address_form.is_valid():
                address = address_form.save(commit=False)
                if not address.user:
                    # for new user that had no address yet its neccessary to set address.user for useraddress obj.
                    address.user = request.user 
                address.save()
                messages.success(request, "آدرس شما با موفقیت به‌روزرسانی شد.")
            else:
                messages.warning(request, "خطا در ذخیره سازی اطلاعات کاربری.لطفااطلاعات را مجدد بررسی فرمایید")
                user_orders = OrderBasket.objects.annotate(items=Count('order_detail')).filter(is_paid=True, user_id=request.user.id)
                user_information_form = self.user_information_form(instance=request.user)

                # Pass the forms with validation errors back to the template
                return render(request, self.template_name, {
                    'user_orders': user_orders,
                    'address_form': self.address_form(request.POST,instance=user_address),
                    'user_information_form': user_information_form,  # Pass the form with errors
                    'user_password_form': self.user_password_form(),
                })
            
        elif 'user-information' in request.POST:
            user_information_form = self.user_information_form(request.POST, instance=request.user)
            if user_information_form.is_valid():
                user_information_form.save()
                messages.success(request, "اطلاعات کاربری شما با موفقیت به‌روزرسانی شد.")
            else:
                messages.warning(request, "خطا در ذخیره اطلاعات کاربری. لطفاً اطلاعات را مجدد بررسی کنید.")
                user_orders = OrderBasket.objects.annotate(items=Count('order_detail')).filter(is_paid=True, user_id=request.user.id)
                user_address = UserAddress.objects.filter(user=request.user).first()

                # Pass the forms with validation errors back to the template
                return render(request, self.template_name, {
                    'user_orders': user_orders,
                    'address_form': self.address_form(instance=user_address),
                    'user_information_form': user_information_form,  # Pass the form with errors
                    'user_password_form': self.user_password_form(),
                })

        elif 'user-password' in request.POST:
            user_password_form = self.user_password_form(request.POST,instance=request.user)

            if user_password_form.is_valid():
                request.user.set_password(user_password_form.cleaned_data["new_password"])
                request.user.save()
                logout(request)
                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد.")
                return redirect(reverse('account_module:user-login'))
            else:
                messages.warning(request, "خطا در تغییر رمز عبور. لطفاً اطلاعات را بررسی کنید.")

        return redirect(reverse('user_profile_module:user-profile'))
    

# @is_authenticated_permission
def user_favorite_products(request):
    user_favorite_products=UserFavoriteProduct.objects.filter(user_id=request.user.id).order_by('product__added_date')

    return render(request,'user_profile_module/user_favorite_list.html',{
        'user_favorite_products':user_favorite_products
    })


def user_order_detail(request,order_id):
    target_order_basket=OrderBasket.objects.prefetch_related('order_detail').filter(id=order_id).first()
    
    return render(request,'user_profile_module/user_profile_order_detail.html',{
        'order':target_order_basket
    })

# done
def remove_user_favorite_product(request):
    product_id=request.GET.get('favorite_product_id')

    user_favorite_product=UserFavoriteProduct.objects.filter(user_id=request.user.id,product_id=product_id).first()
    if user_favorite_product is None:
        return JsonResponse({
            'status':'error'
        })
    user_favorite_product.delete()

    context={
        'user_favorite_products':UserFavoriteProduct.objects.filter(user_id=request.user.id).order_by('product__added_date')
    }

    return JsonResponse({
            'status':'success',
            'body':render_to_string("user_profile_module/includes/user_favorite_component.html",context)
        })


# def change_user_favorite_product_count(request):
    # product_id=request.GET.get('favorite_product_id')
    # state=request.GET.get('state')
    
    # if product_id is None or state is None:
    #     return JsonResponse({
    #         'status':'invalid-request'
    #     })

    # user_favorite_product=UserFavoriteProduct.objects.filter(user_id=request.user.id,product_id=product_id).first()
    # if user_favorite_product is None:
    #     return JsonResponse({
    #         'status':'not-found'
    #     })
    
    
    # context={
    #     'user_favorite_products':UserFavoriteProduct.objects.filter(user_id=request.user.id).order_by('product__added_date')
    # }

    # return HttpResponse('view done')
