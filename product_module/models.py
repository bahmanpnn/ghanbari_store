from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator,MinValueValidator
from django.urls import reverse
from account_module.models import User


class Product(models.Model):
    title=models.CharField(max_length=127,db_index=True,unique=True)
    image=models.ImageField(upload_to="images/products",null=True,blank=True)
    short_description=models.CharField(max_length=510,db_index=True,null=True,blank=True)
    content=models.TextField(null=True,blank=True)
    price=models.PositiveIntegerField()
    weight=models.PositiveIntegerField()
    discount_percent=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)],blank=True,null=True)
    price_with_discount=models.PositiveIntegerField(null=True,blank=True)
    slug=models.SlugField(blank=True,unique=True,null=True,db_index=True,max_length=127,allow_unicode=True)
    is_active=models.BooleanField(default=True)
    is_delete=models.BooleanField(default=False)
    added_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    rating=models.PositiveSmallIntegerField(default=0,validators=[MaxValueValidator(5),MinValueValidator(0)],blank=True,null=True)
    # brand=models.ForeignKey(ProductBrand,)
    # categoies=models.ManyToMany()
    # tags=models.ManyToMany()

    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.title[0:128],allow_unicode=True)
        return super().save(*args, **kwargs)
    
    # def get_absolute_url(self):
    #     return reverse("product-detail", args=[self.slug])



# class ProductImages(models.Model):
#     pass

# class ProductCategory(models.Model):
#     pass

# class ProductTag(models.Model):
#     pass

# class ProductBrand(models.Model):
#     pass