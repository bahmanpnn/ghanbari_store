from django.db import models
# from django.utils.html import mark_safe
# from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field

class Slider(models.Model):
    title=models.CharField(max_length=100)
    text = CKEditor5Field('Text', config_name='default') 
    created_date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    image=models.ImageField(upload_to='sliders/',null=True)
    link_url=models.URLField(null=True,blank=True)
    btn_text=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.title



# class Slider(models.Model):
#     title=models.CharField(max_length=100)
#     text = CKEditor5Field('Text', config_name='default')  # Use CKEditor5Field
#     # text=RichTextField(config_name='default') 
#     # text=RichTextField()
#     # text=models.TextField()
#     created_date=models.DateTimeField(auto_now_add=True)
#     is_active=models.BooleanField(default=False)
#     image=models.ImageField(upload_to='sliders/',null=True)
#     link_url=models.URLField(null=True,blank=True)
#     btn_text=models.CharField(max_length=100,null=True,blank=True)
    
#     def __str__(self):
#         return self.title
    
#     # def display_text(self):
#     #     return mark_safe(self.text)