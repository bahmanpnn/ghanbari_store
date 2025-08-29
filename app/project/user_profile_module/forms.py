from django import forms
from account_module.models import User,UserAddress
from django.core.exceptions import ValidationError


class EditUserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ('province','city','main_address')
        widgets={
            'province':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':' استان خود را وارد کنید',
            }),
            'city':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':' شهر خود را وارد کنید'
            }),
            'main_address':forms.Textarea(attrs={
                'class':'form-control textarea-style ',
                'placeholder':'آدرس محل سکونت خود را وارد کنید',
                'rows':5
            }),
            }

        error_messages={
            'province':{
                'max_length':"این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
                'required':'فیلد استان اجباری می باشد'
            },
            'city':{
                'max_length':"این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
                'required':'فیلد شهر اجباری می باشد'
            },
            'main_address':{
                'required':'فیلد آدرس اجباری می باشد'
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all fields required
        self.fields['province'].required = True
        self.fields['city'].required = True
        self.fields['main_address'].required = True


class EditUserInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام*'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی*'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره همراه*',
                # 'readonly':'readonly',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل*'
            })
        }

        error_messages = {
            'first_name': {
                'max_length': "این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
                'required':"فیلد  نام اجباری می باشد"
            },
            'last_name': {
                'max_length': "این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
                'required':"فیلد نام خانوادگی اجباری می باشد"
            },
            'phone_number': {
                'max_length': "این فیلد بیشتر از 11 کارکتر را نمی پذیرد!!",
                'required':"فیلد شماره تلفن اجباری می باشد"
            },
            'email': {
                'max_length': "این فیلد بیشتر از 63 کارکتر را نمی پذیرد!!",
                'required':"فیلد  ایمیل اجباری می باشد"
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['email'].required = True

        # disabled the phone_number field to user cant change it
        self.fields['phone_number'].disabled = True  

    def clean_email(self):
            email = self.cleaned_data.get('email')
            user_id = self.instance.id 
            check_email = User.objects.filter(email__iexact=email).exclude(id=user_id)
            if check_email.exists():
                # self.add_error('email', 'این ایمیل قبلاً استفاده شده است')
                raise ValidationError('این ایمیل متعلق به حساب دیگری می باشد')
            return email


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': "رمز عبور قبلی"
        })
    )

    new_password = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': "رمز عبور جدید"
        })
    )

    confirm_new_password = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': "تکرار رمز عبور جدید"
        })
    )

    # def __init__(self, *args, **kwargs):
    #     self.instance = kwargs.pop('instance', None)  # Expect instance from the view
    #     if not self.instance:
    #         raise ValueError("User instance is required for ChangePasswordForm")
    #     super().__init__(*args, **kwargs)


    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)  # Pass the user instance
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.check_password(password):
            raise forms.ValidationError('اطلاعات وارد شده صحیح نیست.')
        return password

    def clean_confirm_new_password(self):

        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password==confirm_new_password :
            return new_password
        
        raise ValidationError('رمز عبور جدید با تایید رمز عبور جدید مطابقت ندارد. لطفا مجدد تلاش کنید!!')
    

