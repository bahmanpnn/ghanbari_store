from django import forms


class SearchForm(forms.Form):
    search_blog=forms.CharField(max_length=255,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':"اینجا جستجو کنید"
    }))