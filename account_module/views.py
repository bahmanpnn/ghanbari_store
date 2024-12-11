from django.shortcuts import redirect, render
from django.views import View
from .forms import RegisterModelForm
from account_module.models import User
from django.contrib import messages


class UserRegisterView(View):
    template_name='account_module/register.html'
    form_class=RegisterModelForm

    def get(self,request):
        return render(request,self.template_name,{
            'form':RegisterModelForm()
        })
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            new_user=User.objects.create_user(username=cd['username'],email=cd['email'])
            new_user.set_password(cd['password'])
            new_user.save()

            # todo:add sms/email service to send code for authorization user and phone number
            # messages.success(request,'ثبت نام با موفقیت انجام شد  لطفا ایمیل خود را چک کنید یا کد ارسال شده به شماره همراه خود را وارد کنید')

            messages.success(request,'ثبت نام با موفقیت انجام شد لطفا وارد حساب کاربری خود شوید')
            return redirect("home_module:home-page")
        return render(request,self.template_name,{
            'form':self.form_class(request.POST)
        })