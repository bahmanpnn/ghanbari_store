from django.shortcuts import redirect, render
from django.views import View
from .forms import UserRegisterForm,UserLoginForm
from account_module.models import User
from django.contrib import messages


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

            # todo:add sms/email service to send code for authorization user and phone number
            # messages.success(request,'ثبت نام با موفقیت انجام شد  لطفا ایمیل خود را چک کنید یا کد ارسال شده به شماره همراه خود را وارد کنید')

            messages.success(request,'ثبت نام با موفقیت انجام شد لطفا وارد حساب کاربری خود شوید')
            return redirect("account_module:user-register")
        return render(request,self.template_name,{
            'form':self.form_class(request.POST)
        })
    
class UserLoginView(View):
    template_name='account_module/login.html'
    form_class=UserLoginForm

    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):
        pass
    