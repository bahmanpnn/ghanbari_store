from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class SiteSetting(models.Model):
    site_logo=models.ImageField(upload_to='images/site_logo/',blank=True,null=True)
    is_main_setting=models.BooleanField(default=True)
    phone=models.CharField(max_length=31,blank=True,null=True)
    email=models.EmailField(max_length=31,blank=True,null=True)
    copy_right=CKEditor5Field(blank=True,null=True)
    about_us=CKEditor5Field('Text', config_name='default',blank=True,null=True)
    site_name=models.CharField(max_length=150)
    site_url=models.CharField(max_length=255)

    
    #social media
    facebook=models.URLField(blank=True,null=True)
    whatsup=models.URLField(blank=True,null=True)
    instagram=models.URLField(blank=True,null=True)
    telegram=models.URLField(blank=True,null=True)
    twitter=models.URLField(blank=True,null=True)
    youtube=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.site_name


class BranchLocation(models.Model):
    branch_name=models.CharField(max_length=127,null=True,blank=False)
    branch_address=models.CharField(max_length=511,null=True,blank=False)
    branch_phone=models.CharField(max_length=63,null=True,blank=True)
    site_setting=models.ForeignKey(SiteSetting,on_delete=models.CASCADE,null=True,blank=False,related_name='branches')


    def __str__(self):
        return f'{self.branch_name} '


