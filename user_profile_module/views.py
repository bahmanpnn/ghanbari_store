from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import login
from account_module.models import User,UserAddress
from order_module.models import OrderBasket
from .forms import EditUserAddressForm,EditUserInformationForm,ChangePasswordForm
from .models import UserFavoriteProduct
# from permissions import is_authenticated_permission
# from django.utils.decorators import method_decorator


class UserProfileView(View):
    template_name = 'user_profile_module/user_profile.html'
    address_form = EditUserAddressForm
    user_information_form = EditUserInformationForm
    user_password_form = ChangePasswordForm

    def get(self, request):
        user_orders = OrderBasket.objects.annotate(items=Count('order_detail')).filter(is_paid=True, user_id=request.user.id)
        user_address = UserAddress.objects.filter(user=request.user).first()

        return render(request, self.template_name, {
            'user_orders': user_orders,
            'address_form': self.address_form(instance=user_address),
            'user_information_form': self.user_information_form(instance=request.user),
            'user_password_form': self.user_password_form(),
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
            user_password_form = self.user_password_form(request.POST)

            if user_password_form.is_valid():
                request.user.set_password(user_password_form.cleaned_data["new_password"])
                request.user.save()
                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد.")
                return redirect(reverse('account_module:user-login'))  # Redirect to login after password change
            else:
                messages.error(request, "خطا در تغییر رمز عبور. لطفاً اطلاعات را بررسی کنید.")

        return redirect(reverse('user_profile_module:user-profile'))


# @is_authenticated_permission
def user_favorite_products(request):
    user_favorite_products=UserFavoriteProduct.objects.filter(user_id=request.user.id).order_by('product__added_date')

    return render(request,'user_profile_module/user_favorite_list.html',{
        'user_favorite_products':user_favorite_products
    })



# @method_decorator(is_authenticated_permission,name='dispatch')
# class UserProfileView(View):
#     template_name = 'user_profile_module/user_profile.html'
#     user_information_form = EditUserInformationForm
#     address_form = EditUserAddressForm

#     def get(self, request):
#         user_orders = OrderBasket.objects.annotate(items=Count('order_detail')).filter(is_paid=True, user_id=request.user.id)
#         user_address = UserAddress.objects.filter(user=request.user).first()  # Safely get the user's address

#         return render(request, self.template_name, {
#             'user_orders': user_orders,
#             'address_form': self.address_form(instance=user_address),
#             'user_information_form': self.user_information_form(instance=request.user)
#         })

#     def post(self, request):
#         if 'user-address' in request.POST:
#             # Fetch the user's address instance
#             user_address = UserAddress.objects.filter(user=request.user).first()
#             address_form = self.address_form(request.POST, instance=user_address)

#             if address_form.is_valid():
#                 # Save the form with the associated user
#                 address = address_form.save(commit=False)
#                 address.user = request.user
#                 address.save()
#                 messages.success(request, 'Address updated successfully.')
#             else:
#                 messages.error(request, 'Invalid address form data.')
#         elif 'user-information' in request.POST:
#             user = request.user 
#             form = EditUserInformationForm(request.POST, instance=user)

#             if form.is_valid():
#                 # Todo:move checking password to forms with clean_password for validation checks
#                 password = form.cleaned_data.get('password')
                
#                 if user.check_password(password):
#                     # Update the user's information
#                     user.first_name = form.cleaned_data.get('first_name')
#                     user.last_name = form.cleaned_data.get('last_name')
#                     user.phone_number = form.cleaned_data.get('phone_number')
#                     user.email = form.cleaned_data.get('email')

#                     # Update the password if a new one is provided
#                     new_password = form.cleaned_data.get('new_password')
#                     if new_password:
#                         user.set_password(new_password)

#                     user.save()
#                     messages.success(request, 'اطلاعات شما با موفقیت به‌روزرسانی شد.')

#                     # Re-authenticate user if password changed
#                     if new_password:
#                         login(request,user)
#                 else:
#                     messages.error(request, 'رمز عبور فعلی نادرست است.')
#                     return redirect(reverse('user_profile_module:user-profile'))
#                 return redirect(reverse('user_profile_module:user-profile'))
#             else:
#                 messages.error(request, 'فرم دارای خطا است. لطفاً دوباره تلاش کنید.')

#         return redirect(reverse('user_profile_module:user-profile'))


# class UserProfileView(View):
#     template_name = 'user_profile_module/user_profile.html'
#     user_information_form = EditUserInformationForm
#     address_form = EditUserAddressForm

#     def get(self, request):
#         user_orders = OrderBasket.objects.annotate(items=Count('order_detail')).filter(is_paid=True, user_id=request.user.id)
#         user_address = UserAddress.objects.filter(user=request.user).first()  # Safely get the user's address

#         return render(request, self.template_name, {
#             'user_orders': user_orders,
#             'address_form': self.address_form(instance=user_address),
#             'user_information_form': self.user_information_form(instance=request.user)
#         })

#     def post(self, request):
#         if 'user-address' in request.POST:
#             # Fetch the user's address instance
#             user_address = UserAddress.objects.filter(user=request.user).first()
#             address_form = self.address_form(request.POST, instance=user_address)

#             if address_form.is_valid():
#                 # Save the form with the associated user
#                 address = address_form.save(commit=False)
#                 address.user = request.user
#                 address.save()
#                 messages.success(request, 'Address updated successfully.')
#             else:
#                 messages.error(request, 'Invalid address form data.')

#         # todo:complete user info saving and check user wants to change password or not
#         # todo:check user wants to change phone number or not if phone number changed send sms for new phone number to authenticate it.
#         elif 'user-information' in request.POST:
#             form = self.user_information_form(request.POST, instance=request.user)
#             # user=User.objects.filter(id=request.user.id)
#             if form.is_valid():
#                 cd=form.cleaned_data
#                 if cd['new_password']== "" and cd['confirm_new_password'] =="":
#                     print('user didnt change password')
#                 else:
#                     print('user changed password')


#                 messages.success(request, 'User information updated successfully.')
#             else:
#                 messages.error(request, 'Invalid user information form data.')

#         return redirect(reverse('user_profile_module:user-profile'))

