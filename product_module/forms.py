from django import forms

class ProductFilterForm(forms.Form):
    PRODUCT_FILTERING_CHOICES = [
        ('all', 'همه محصولات'),
        ('discounted', 'محصولات تخفیف خورده'),
        ('no-discount', 'محصولات بدون تخفیف'),
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
