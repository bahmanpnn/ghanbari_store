from django import forms
from account_module.models import User
from django.core.exceptions import ValidationError
import re

class RegisterModelForm(forms.Form):
    # todo change username with phone number 
    username=forms.CharField(max_length=63,widget=forms.TextInput(attrs=
                                        {'placeholder':"نام کاربری"})
                                    )
    email=forms.CharField(max_length=63,widget=forms.TextInput(attrs=
                                        {'placeholder':"ایمیل"})
                                    )
    password=forms.CharField(max_length=63,widget=forms.PasswordInput(attrs=
                                        {'placeholder':"رمز عبور"})
                                    )
    confirm_password=forms.CharField(max_length=63,widget=forms.PasswordInput(attrs=
                                        {'placeholder':"تکرار رمز عبور"})
                                    )

    def clean_email(self):
        email=self.cleaned_data.get('email')
        check_email=User.objects.filter(email__iexact=email)
        if check_email:
            print('این پست الکترونیک قبلا استفاد شده است')
            raise ValidationError('این پست الکترونیک قبلا استفاده شده است')
        
        return email
    
    # todo change username with phone number 
    def clean_username(self):
        username=self.cleaned_data.get('username')
        check_username=User.objects.filter(username__iexact=username)
        if check_username:
            print('این نام کاربری قبلا استفاده شده است')
            raise ValidationError('این نام کاربری قبلا استفاده شده است')

        return username
    

    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            print('رمز عبور با تکرار آن مطابقت ندارد')
            raise ValidationError('رمز عبور با تکرار آن مطابقت ندارد')
        
        return confirm_password


    def is_strong_password(password):
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


    
