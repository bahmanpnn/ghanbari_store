from django import forms
from .models import ContactModel, ContactSubjectItem


class ContactForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=ContactSubjectItem.objects.all(),
        label="موضوع",
        empty_label="همه دسته بندی‌ها",
        # widget=forms.Select(attrs={'class': 'text-center'})
    )

    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'subject', 'text']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام شما'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل شما'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'پیام شما'})
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subject'].widget.attrs.update({'class': 'form-select'})
