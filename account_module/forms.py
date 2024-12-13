from django import forms
from account_module.models import User
from django.core.exceptions import ValidationError
import re

class UserRegisterForm(forms.Form):
    # todo change username with phone number 
    phone_number=forms.CharField(max_length=63,widget=forms.TextInput(attrs=
                                        {'placeholder':" شماره تلفن خود را وارد کنید"})
                                    )
    email=forms.CharField(max_length=63,required=False,widget=forms.TextInput(attrs=
                                        {'placeholder':"ایمیل خود را وارد کنید"})
                                    )
    password=forms.CharField(max_length=63,widget=forms.PasswordInput(attrs=
                                        {'placeholder':"رمز عبور خود را وارد کنید"})
                                    )
    confirm_password=forms.CharField(max_length=63,widget=forms.PasswordInput(attrs=
                                        {'placeholder':"تکرار رمز عبور خود را وارد کنید"})
                                    )

    def clean_email(self):
        email=self.cleaned_data.get('email')
        print(email)
        if email:
            check_email=User.objects.filter(email__iexact=email)
            if check_email:
                print('این پست الکترونیک قبلا استفاد شده است')
                raise ValidationError('این پست الکترونیک قبلا استفاده شده است')    
        return email
    
    def clean_phone_number(self):
        phone_number=self.cleaned_data.get('phone_number')
        check_phone_number=User.objects.filter(phone_number__iexact=phone_number)
        if check_phone_number:
            # print('این شماره تلفن قبلا استفاده شده است')
            raise ValidationError('این شماره تلفن قبلا استفاده شده است')

        return phone_number
    
    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            print('رمز عبور با تکرار آن مطابقت ندارد')
            raise ValidationError('رمز عبور با تکرار آن مطابقت ندارد')
        elif not self.is_strong_password(password):
            raise ValidationError('رمز عبور شما قوی نمی باشد\
                                  .لطفا ازحروف کوچک و بزرگ به همراه اعداد و سمبل ها استفاده کنید')
        # print('this is password',password)
        return confirm_password

    def is_strong_password(self,password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):  # At least one uppercase letter
            return False
        if not re.search(r"[a-z]", password):  # At least one lowercase letter
            return False
        if not re.search(r"[0-9]", password):  # At least one digit
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # At least one special character
            return False
        return True

    
class UserLoginForm(forms.Form):

    email_or_phone_number=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control text-center',
        'placeholder':'ایمیل یا رمز عبور خود را وارد کنید'
    }))

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control text-center',
        'placeholder':'رمز عبور خود را وارد کنید'
    }))


    # todo:check ip that dont try more than 5 times that fill password wrong in every 1 hour(throttle)
    # def clean_email_or_phone_number(self): 
    #     '''
    #         this is for validation email or phone number field of login
    #     '''
    #     email_or_phone_number=self.cleaned_data.get('email_or_phone_number')
    #     check_phone_number=User.objects.filter(phone_number__iexact=email_or_phone_number).exists()
    #     if check_phone_number:
    #         return email_or_phone_number
    #     else:
    #         check_email=User.objects.filter(email__iexact=email_or_phone_number).exists()
    #         if check_email:
    #             return email_or_phone_number
    #         else:
    #             raise ValidationError('این شماره تلفن یا ایمیل ثبت نشده است')


        

    
