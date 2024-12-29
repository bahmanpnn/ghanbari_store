from django import forms
from account_module.models import User,UserAddress


class EditUserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = ('province','city','main_address')
        widgets={
            'province':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':' استان خود را وارد کنید'
            }),
            'city':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':' شهر خود را وارد کنید'
            }),
            'main_address':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'آدرس محل سکونت خود را وارد کنید'
            }),
            }

        error_messages={
            'province':{
                'max_length':"این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
                'required':'این فیلد اجباری می باشد'
            },
            'city':{
                'max_length':"این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
                'required':'این فیلد اجباری می باشد'
            },
            'main_address':{
                'required':'این فیلد اجباری می باشد'
            }
        }


class EditUserInformationForm(forms.ModelForm):
    new_password=forms.CharField(max_length=63,
                                    required=False,
                                    widget=forms.PasswordInput(attrs=
                                    {'placeholder':"رمز عبور جدید خود را وارد کنید"})
                                )
    confirm_new_password=forms.CharField(max_length=63,
                                            required=False,
                                            widget=forms.PasswordInput(attrs=
                                            {'placeholder':"تکرار رمز عبور جدید خود را وارد کنید"})
                                        )

    class Meta:
        model = User
        fields = ('first_name','last_name','phone_number','email','password','new_password','confirm_new_password')
        widgets={
            'first_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':' نام*'
            }),
            'last_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':' نام خانوادگی*'
            }),
            'phone_number':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':' شماره همراه*'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':' ایمیل*'
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'رمز عبور*'
            })
            }

        # error_messages={
        #     'province':{
        #         'max_length':"این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
        #         'required':'این فیلد اجباری می باشد'
        #     },
        #     'city':{
        #         'max_length':"این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
        #         'required':'این فیلد اجباری می باشد'
        #     },
        #     'main_address':{
        #         'required':'این فیلد اجباری می باشد'
        #     }
        # }

