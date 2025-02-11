from django import forms
from .models import ProductCommentReview


class ProductFilterForm(forms.Form):
    PRODUCT_FILTERING_CHOICES = [
        ('all', 'همه محصولات'),
        ('discounted', 'محصولات تخفیف خورده'),
        # ('no-discount', 'محصولات بدون تخفیف'),
        ('most-bought', 'محصولات پرطرفدار'),
    ]
    product_filter = forms.ChoiceField(choices=PRODUCT_FILTERING_CHOICES,
                                        label='',
                                        required=False,
                                        widget=forms.Select(attrs={
                                            'name':"sort",
                                            'id':"sort",
                                            'onchange':"updateSorting()"
                                            }))
    # product_filter = forms.ChoiceField(choices=PRODUCT_FILTERING_CHOICES,label='',required=False, widget=forms.Select())


class ProductCommentReviewForm(forms.ModelForm):
    PRODUCT_RATING_CHOICES = [
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    ]
    
    product_rating = forms.ChoiceField(
        choices=PRODUCT_RATING_CHOICES,
        label='',
        required=True,
        widget=forms.Select(attrs={
            'class': 'rating-dropdown',  # Add class for styling
            'name': "rating",
            'id': "rating",
        })
    )
    # description = forms.CharField(
    #     widget=forms.Textarea(attrs={
    #         'id':'description'
    #     })
    # )
    class Meta:
        model = ProductCommentReview
        fields = ["product_rating", "description"]




# class ProductCommentReviewForm(forms.Form):
#     PRODUCT_RATING_CHOICES = [
#         ('5', '5'),
#         ('4', '4'),
#         ('3', '3'),
#         ('2', '2'),
#         ('1', '1'),
#     ]
#     product_rating = forms.ChoiceField(choices=PRODUCT_RATING_CHOICES,
#                                         label='',
#                                         required=True,
#                                         widget=forms.Select(attrs={
#                                             'name':"product_rating",
#                                             'id':"product_rating",
#                                             }))
#     description=forms.CharField(widget=forms.Textarea(attrs={
#         'class':'form-control',
#         'placeholder':'متن پیام شما',
#         'rows':4,
#     }))


# class ProductCommentReviewForm(forms.ModelForm):
#     class Meta:
#         model = ProductCommentReview
#         fields = ["rating", "description"]
#         widgets = {
#             "rating": forms.Select(choices=[
#                 ('5', '5'),
#                 ('4', '4'),
#                 ('3', '3'),
#                 ('2', '2'),
#                 ('1', '1'),
#             ], attrs={'name': "rating", 'id': "rating"})
#         }



# class ProductCommentReviewForm(forms.ModelForm):
#     class Meta:
#         model = ProductCommentReview
#         fields = ["rating", "description"]  # Exclude user fields

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)  # Get user from view
#         super().__init__(*args, **kwargs)

#         if self.user and self.user.is_authenticated:
#             self.fields['rating'].widget.attrs.update({'class': 'form-control'})  # Example styling

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if self.user and self.user.is_authenticated:
#             instance.user = self.user  # Assign the logged-in user
#         if commit:
#             instance.save()
#         return instance
