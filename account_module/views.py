from django.shortcuts import redirect, render
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import login,logout
from account_module.models import User
from .forms import UserRegisterForm,UserLoginForm,UserOtpCodeForm
from .models import UserOTP


class UserRegisterView(View):
    template_name='account_module/register.html'
    form_class=UserRegisterForm

    def get(self,request):
        return render(request,self.template_name,{
            'form':UserRegisterForm()
        })
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            if not cd['email']:
                new_user=User(username=cd['phone_number'],phone_number=cd['phone_number'])
            else:    
                new_user=User(username=cd['email'],phone_number=cd['phone_number'],email=cd['email'])
            new_user.set_password(cd['password'])
            new_user.save()
            otp_instance, created = UserOTP.objects.get_or_create(user=new_user)
            otp_instance.generate_otp()
            # todo:send otp to phone number
            # print(otp_instance.otp)

            # todo:send this message with js
            messages.success(request,'ثبت نام با موفقیت انجام شد  لطفا کد ارسال شده به شماره همراه خود را وارد کنید')

            return redirect("account_module:user-otp-code")
        return render(request,self.template_name,{
            'form':self.form_class(request.POST)
        })
    

class UserOtpCode(View):
    template_name='account_module/test_user_otp.html'
    form_class=UserOtpCodeForm

    def get(self,request):
        return render(request,self.template_name,{
            'form':self.form_class()
        })
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            otp_code=cd['input1']+cd['input2']+cd['input3']+cd['input4']+cd['input5']+cd['input6']
            print(otp_code)
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
            check_user_phone_number=User.objects.filter(phone_number=cd['email_or_phone_number']).first()
            check_user_email=User.objects.filter(email__iexact=cd['email_or_phone_number']).first()
            if check_user_phone_number:
                if check_user_phone_number.check_password(cd['password']):
                    login(request,check_user_phone_number)
                    messages.success(request,'به خوشه خوش آمدید')
                    return redirect('home_module:home-page')
                else:
                    # messages.error(request,'رمز عبور اشتباه است',extra_tags='danger')
                    form.add_error('password',error='رمز عبور اشتباه است')
                    return render(request,self.template_name,{
                        'form':form
                    })
            elif check_user_email:
                if check_user_email.check_password(cd['password']):
                    login(request,check_user_email)
                    # login(request,check_user_email,backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request,'به خوشه خوش آمدید')
                    return redirect('home_module:home-page')  
                else:
                    # todo:send error msg with js
                    # messages.error(request,'رمز عبور اشتباه است',extra_tags='danger')
                    form.add_error('password',error='رمز عبور اشتباه است')
                    return render(request,self.template_name,{
                        'form':form
                    }) 
            else:
                form.add_error('password','این ایمیل یا شماره تلفن وجود ندارد')
                return render(request,self.template_name,{
                        'form':form
                    })
        return render(request,self.template_name,{
            'form':self.form_class(request.POST)
        })
            

class UserLogOutView(View):
    # todo:add permission that user is authenticated
    def get(self,request):
        logout(request)
        messages.success(request,'از حساب خود با موفقیت خاج شدید')
        return redirect('home_module:home-page')
    