from datetime import datetime, timedelta
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator,MinValueValidator
from django.urls import reverse
from account_module.models import User
from django_ckeditor_5.fields import CKEditor5Field


# class Product(models.Model):
#     title = models.CharField(max_length=127, db_index=True, unique=True)
#     quantity = models.PositiveIntegerField(default=0)
#     image = models.ImageField(upload_to="images/products", null=True, blank=True)
#     short_description = models.CharField(max_length=510, db_index=True, null=True, blank=True)
#     content = CKEditor5Field('Text', config_name='default', null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     weight = models.DecimalField(max_digits=10, decimal_places=2)
#     calorie = models.PositiveIntegerField(null=True, blank=True)
#     avg_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
#     discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)], blank=True, null=True)
#     slug = models.SlugField(blank=True, unique=True, null=True, db_index=True, max_length=127, allow_unicode=True)
#     is_active = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#     added_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title, allow_unicode=True)
#         super().save(*args, **kwargs)

class Product(models.Model):
    title=models.CharField(max_length=127,db_index=True,unique=True)
    quantity=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="images/products",null=True,blank=True)
    short_description=models.CharField(max_length=510,db_index=True,null=True,blank=True)
    content = CKEditor5Field('Text', config_name='default',null=True,blank=True) 
    price=models.PositiveIntegerField()
    weight=models.PositiveIntegerField()
    calorie=models.IntegerField(null=True,blank=True)
    # avg_rate=models.FloatField(default=0.0)
    avg_rate = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    discount_percent=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)],blank=True,null=True)
    price_with_discount=models.PositiveIntegerField(null=True,blank=True)
    slug=models.SlugField(blank=True,unique=True,null=True,db_index=True,max_length=127,allow_unicode=True)
    is_active=models.BooleanField(default=True)
    is_delete=models.BooleanField(default=False)
    added_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.title[0:128],allow_unicode=True)
        return super().save(*args, **kwargs)
    
    # def get_absolute_url(self):
    #     return reverse("product-detail", args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="images/products/extra-images")

    def __str__(self):
        return f"Image for {self.product.title}"


def default_end_date():
    """Function to calculate the default end date."""
    return datetime.now() + timedelta(days=7)

class ProductOfTheWeek(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="weekly_highlight")
    title = models.CharField(max_length=127)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=default_end_date)  # Refer to the static method here
    is_active_bool = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    background_image=models.ImageField(upload_to="images/product_of_the_week/",null=True,blank=True)

    @staticmethod
    def default_end_date():
        return datetime.now() + timedelta(days=7)

    def is_active(self):
        now = datetime.now()
        return self.start_date <= now <= self.end_date

    # def __str__(self):
    #     return f"{self.product.title} {self.discount_percentage}"


class CommentReviewStatusType(models.IntegerChoices):
    pending=1,'در انتظار تایید'
    accepted=2,'پذیرش شده'
    rejected=3,'رد شده'


class ProductCommentReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    description=models.TextField()
    rating=models.IntegerField(default=5,validators=[MaxValueValidator(5),MinValueValidator(0)],blank=True,null=True)
    status=models.IntegerField(choices=CommentReviewStatusType.choices,default=CommentReviewStatusType.pending.value)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)


