from django import forms
from .models import ContactModel, ContactSubjectItem


class ContactForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=ContactSubjectItem.objects.all(),
        label="موضوع",
        empty_label="همه دسته بندی‌ها",
        widget=forms.Select(attrs={'class': 'form-control custom-select'}),
        required=True,
        error_messages={
            'required': 'لطفاً موضوع پیغام خود را انتخاب کنید',
        }
    )

    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'subject', 'text']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام شما'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل شما'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'پیام شما'})
        }
        error_messages = {
            'name': {
                'required': "وارد کردن نام خود اجباری می باشد",
            },
            'email': {
                'required': "وارد کردن ایمیل برای دریافت پاسخ اجباری می باشد",
            },
            'text': {
                'required': "وارد کردن متن پیام خود اجباری می باشد",
            }
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subject'].widget.attrs.update({'class': 'form-select'})
