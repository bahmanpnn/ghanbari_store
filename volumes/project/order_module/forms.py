from django import forms
from account_module.models import User,UserAddress
from .models import Checkout



class CheckOutForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    province = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    main_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    about_order_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Checkout
        fields = [
            'phone_number', 'email', 'first_name', 'last_name', 
            'province', 'city', 'main_address', 'zip_code', 'about_order_text'
        ]

    def __init__(self, *args, user=None, checkout_instance=None, **kwargs):
        """Prefill form fields from User and Checkout instance"""
        super().__init__(*args, **kwargs)

        if user:
            # Prefill from User model
            self.fields['phone_number'].initial = user.phone_number
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

        if checkout_instance:
            # Prefill from existing checkout instance
            for field in self.fields:
                if hasattr(checkout_instance, field):
                    self.fields[field].initial = getattr(checkout_instance, field)
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get("zip_code")
        if not zip_code.isdigit():
            raise forms.ValidationError("Zip code must contain only digits.")
        return zip_code



# class CheckOutForm(forms.ModelForm):
#     phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     province = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     main_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     about_order_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),required=False)

#     class Meta:
#         model = Checkout
#         fields = [
#             'phone_number', 'email', 'first_name', 'last_name', 
#             'province', 'city', 'main_address', 'zip_code', 'about_order_text'
#         ]

#     def __init__(self, *args, user=None, **kwargs):
#         """Prefill form fields from User and UserAddress models"""
#         super().__init__(*args, **kwargs)
        
#         if user:
#             # Prefill from User model
#             self.fields['phone_number'].initial = user.phone_number
#             self.fields['email'].initial = user.email
#             self.fields['first_name'].initial = user.first_name
#             self.fields['last_name'].initial = user.last_name
            
#             # Prefill from UserAddress model (if exists)
#             user_address = user.user_address.first()
#             if user_address:
#                 self.fields['province'].initial = user_address.province
#                 self.fields['city'].initial = user_address.city
#                 self.fields['main_address'].initial = user_address.main_address




















# class CheckOutForm(forms.ModelForm):
#     phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     about_order_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

#     class Meta:
#         model = UserAddress  # Base model is UserAddress
#         fields = ['province', 'city', 'main_address']  # Fields from UserAddress
#         widgets = {
#             'province': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'main_address': forms.TextInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop("user", None)  # Get user instance
#         super().__init__(*args, **kwargs)

#         if user:
#             # Fill from User model
#             self.fields["phone_number"].initial = user.phone_number
#             self.fields["email"].initial = user.email
#             self.fields["first_name"].initial = user.first_name
#             self.fields["last_name"].initial = user.last_name

#             # disable phone_number because it belongs to user
#             # self.fields['phone_number'].disabled = True 

#             # Fill from UserAddress (first address if available)
#             address = user.user_address.first()
#             if address:
#                 self.instance = address  # Set instance to existing address













# class CheckOutForm(forms.ModelForm):
#     phone_number=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control'
#     }))

#     email=forms.EmailField(widget=forms.EmailInput(attrs={
#         'class':'form-control'
#     }))

#     first_name=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control'
#     }))

#     last_name=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control'
#     }))

#     province=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control'
#     }))

#     city=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control'
#     }))

#     main_address=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control'
#     }))

#     zip_code=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control'
#     }))
    
#     about_order_text=forms.CharField(widget=forms.Textarea(attrs={
#         'class':'form-control'
#     }))

#     class Meta:
#         model=User
#         fields=["phone_number"]

#         # widgets={
#         #     'phone_number':forms.TextInput(attrs={
#         #         'class':'form-control',
#         #         'placeholder':' شماره تلفن خود را وارد کنید',
#         #     })
#         #     }

