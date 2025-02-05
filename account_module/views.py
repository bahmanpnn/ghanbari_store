from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import login,logout
from django.core.cache import cache
from django.http import JsonResponse
from account_module.models import User
from .forms import UserRegisterForm,UserLoginForm,UserOtpCodeForm,UserForgetPasswordForm,\
                    UserChangePasswordForm
from .models import UserOTP


class UserRegisterView(View):
    template_name='account_module/register.html'
    form_class=UserRegisterForm

    def get(self,request):
        return render(request,self.template_name,{
            'form':self.form_class()
        })
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data

            if User.objects.filter(phone_number=cd['phone_number']).exists():
                # messages.error(request, 'این شماره تلفن قبلا استفاده شده است')
                form.add_error('phone_number', 'این شماره تلفن قبلا استفاده شده است')
                return render(request, self.template_name, {'form': form})
            
            new_user = User(username=cd['phone_number'] if not cd['email'] else cd['email'],
                            phone_number=cd['phone_number'],
                            email=cd.get('email', '')
                            )
            
            new_user.set_password(cd['password'])
            new_user.save()


            # if not cd['email']:
            #     new_user=User(username=cd['phone_number'],phone_number=cd['phone_number'])
            # else:    
            #     new_user=User(username=cd['email'],phone_number=cd['phone_number'],email=cd['email'])

            otp_instance, created = UserOTP.objects.get_or_create(
                user=new_user,
                defaults={'otp': '453241'}  # Set a placeholder for OTP
            )
            if created:
                otp_instance.generate_otp()
                
            if not created and not otp_instance.is_valid():
                otp_instance.generate_otp()

            cache.set(f"otp:{cd['phone_number']}", otp_instance.otp, timeout=900)
            print(request.session.session_key)
            cache.set(f"phone_number:{request.session.session_key}", cd['phone_number'], timeout=900)

            # todo:send otp to phone number with sms provider
            print(f"Generated OTP: {otp_instance.otp}")
            # print(otp_instance.is_valid())
            # print(otp_instance.send_otp())
            
            # todo:send this message with js
            messages.success(request,'ثبت نام با موفقیت انجام شد  لطفا کد ارسال شده به شماره همراه خود را وارد کنید')

            return redirect(f"{reverse('account_module:user-otp-code')}?flow=signup")

        return render(request,self.template_name,{
            'form':self.form_class(request.POST)
        })
    

class UserOtpCode(View):
    template_name='account_module/test_user_otp.html'
    form_class=UserOtpCodeForm

    def get(self,request):
        flow_type = request.GET.get("flow", "signup")  # Default to signup
        return render(request,self.template_name,{
            'form':self.form_class(),
            'flow_type':flow_type
        })
    
    def post(self,request):
        form=self.form_class(request.POST)
        flow_type = request.GET.get("flow", "signup")

        if form.is_valid():
            cd=form.cleaned_data
            session_key = request.session.session_key
            # print('session_key= ',session_key)
            phone_number = cache.get(f"phone_number:{session_key}")
            # print('phone_number = cache.get(f"phone_number:{session_key}")',phone_number)

            if not phone_number:
                return JsonResponse({'error': 'Session expired. Please sign up again.'}, status=400)
            
            cached_otp = cache.get(f"otp:{phone_number}")
            if not cached_otp:
                messages.error(request, "کد تایید منقضی شده است. لطفاً دوباره درخواست ارسال کنید.")
                return redirect("account_module:user-forget-password")

            # print('cached_otp = cache.get(f"otp:{phone_number}")',cached_otp)
            # if not cached_otp:
            #     return JsonResponse({'error': 'OTP expired. Please request a new one.'}, status=400)
        
            # otp_code=cd['input1']+cd['input2']+cd['input3']+cd['input4']+cd['input5']+cd['input6']
            otp_code = ''.join([cd[f'input{i}'] for i in range(1, 7)])

            if otp_code == cached_otp:
                # OTP is valid; mark the user as verified
                user = User.objects.get(phone_number=phone_number)
                user.is_verified = True
                user.save()
                
                # Remove OTP and phone number from Redis
                # cache.delete(f"otp:{otp_code}") # my mind says its better and more true!
                cache.delete(f"otp:{phone_number}")
                cache.delete(f"phone_number:{session_key}")

                # Check flow type and redirect user 
                if flow_type == "signup":
                    messages.success(request,'حساب کابری شما تایید شد حالا میتوانید به حساب خود وارد شوید')
                    return redirect(reverse('account_module:user-login'))
                elif flow_type == "forget_password":
                    cache.set(f"verified_user:{request.session.session_key}", phone_number, timeout=900)
                    messages.success(request,'حساب کابری شما تایید شد لطفا رمز عبور جدید خود را وارد کنید')
                    return redirect(reverse('account_module:user-change-password'))
            else:
                messages.error(request, 'کد تایید نامعتبر است لطفا مجدد امتحان کنید')

            # return JsonResponse({'message': 'Phone number verified successfully.'})
        # return JsonResponse({'error': 'Invalid OTP. Please try again.'}, status=400)
        # else:
        #     print(form.errors)
        return render(request,self.template_name,{
            'form':self.form_class()
        })


class UserLoginView(View):
    template_name='account_module/login.html'
    form_class=UserLoginForm

    def get(self,request):
        return render(request,self.template_name,{
            'form':self.form_class()
        })
    
    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            user=User.objects.filter(phone_number=cd['phone_number']).first()

            if user: # user is not None
                if user.check_password(cd['password']):
                    if user.is_verified:
                        login(request,user)
                        messages.success(request,'به خوشه خوش آمدید')
                        return redirect('home_module:home-page')
                    else:
                        otp_instance, created = UserOTP.objects.get_or_create(
                            user=user,
                            defaults={'otp': '453241'}  # Set a placeholder for OTP
                        )
                        if created:
                            otp_instance.generate_otp()
                            
                        if not created and not otp_instance.is_valid():
                            otp_instance.generate_otp()

                    cache.set(f"otp:{cd['phone_number']}", otp_instance.otp, timeout=900)
                    cache.set(f"phone_number:{request.session.session_key}", cd['phone_number'], timeout=900)

                    # todo:send otp to phone number with sms provider
                    print(f"Generated OTP: {otp_instance.otp}")
                    
                    # todo:send this message with js
                    messages.success(request,'حساب شما برای فعالسازی نیاز به احراز هویت و تایید کد ارسال شده دارد')

                    return redirect(f"{reverse('account_module:user-otp-code')}?flow=signup")
                
                else:
                    # messages.error(request,'رمز عبور اشتباه است',extra_tags='danger')
                    form.add_error('password',error='رمز عبور اشتباه است')
                    return render(request,self.template_name,{
                        'form':form
                    })
            else:
                form.add_error('password','شماره تلفن وارد شده یافت نشد')
                return render(request,self.template_name,{
                        'form':form
                    })
        return render(request,self.template_name,{
            'form':self.form_class(request.POST)
        })
            

class UserForgetPasswordView(View):
    template_name='account_module/forget_password.html'
    form_class=UserForgetPasswordForm

    def get(self,request):
        return render(request,self.template_name,{
            'form':self.form_class()
        })

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data

            checked_user=User.objects.filter(phone_number__exact=cd['phone_number']).first()

            if not checked_user:
                form.add_error('phone_number','این شماره تلفن در خوشه وجود ندارد!')
                return render(request,self.template_name,{
                        'form':form
                    })
            
            otp_instance, created = UserOTP.objects.get_or_create(
                user=checked_user,
                defaults={'otp': '453241'}  # Set a placeholder for OTP
            )
            if created:
                otp_instance.generate_otp()
                
            if not created and not otp_instance.is_valid():
                otp_instance.generate_otp()

            cache.set(f"otp:{cd['phone_number']}", otp_instance.otp, timeout=900)
            cache.set(f"phone_number:{request.session.session_key}", cd['phone_number'], timeout=900)

            # todo:send otp to phone number with sms provider
            print(f"Generated OTP: {otp_instance.otp}")
            
            # todo:send this message with js
            messages.success(request,'لطفا کد ارسال شده به شماره تلفن خود را وارد کنید')

            # return redirect("account_module:user-otp-code")
            return redirect(f"{reverse('account_module:user-otp-code')}?flow=forget_password")

        
        return render(request,self.template_name,{
            'form':self.form_class(request.POST)
        },status=400)
    

class UserChangePasswordView(View):
    template_name = "account_module/change_password.html"
    form_class = UserChangePasswordForm

    def get(self, request):
        session_key = request.session.session_key
        phone_number = cache.get(f"verified_user:{session_key}")

        check_user=User.objects.filter(phone_number=phone_number).first()

        if check_user is None:
            return JsonResponse({'error': 'دسترسی غیرمجاز! لطفاً دوباره درخواست بازیابی رمز عبور را ارسال کنید.'}, status=400)
        
        
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        session_key = request.session.session_key
        phone_number = cache.get(f"verified_user:{session_key}")



        if not phone_number:
            # return JsonResponse({'error': 'دسترسی غیرمجاز! لطفاً دوباره درخواست بازیابی رمز عبور را ارسال کنید.'}, status=400)
            messages.error(request, "دسترسی غیرمجاز! لطفاً دوباره درخواست بازیابی رمز عبور را ارسال کنید.")
            return redirect("account_module:forget-password")
        

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            check_user=User.objects.filter(phone_number=phone_number).first()

            if check_user is None:
                messages.error(request, "کاربر یافت نشد. لطفاً دوباره امتحان کنید.")
                return redirect("account_module:forget-password")

            check_user.set_password(cd["confirm_password"])
            check_user.save()

            # Clear Redis key after successful password reset
            cache.delete(f"verified_user:{request.session.session_key}")

            messages.success(request, "رمز عبور با موفقیت تغییر کرد. لطفاً وارد شوید.")
            return redirect("account_module:user-login")

        return render(request, self.template_name, {"form": form})


class UserLogOutView(View):
    # todo:add permission that user is authenticated
    def get(self,request):
        logout(request)
        messages.success(request,'از حساب خود با موفقیت خاج شدید')
        return redirect('home_module:home-page')










# def resend_otp_view(request):
#     if request.method == "POST":
#         phone_number = request.POST.get('phone_number')
        
#         # Generate a new OTP and update it in Redis
#         otp_code = generate_otp()
#         cache.set(f"otp:{phone_number}", otp_code, timeout=900)  # Reset expiration time
#         send_otp(phone_number, otp_code)
        
#         return JsonResponse({'message': 'A new OTP has been sent to your phone number.'})

