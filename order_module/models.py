from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from account_module.models import User
from product_module.models import Product
from site_settings_module.models import SiteSetting
from django.utils.timezone import now



class OrderBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    # discount = models.PositiveIntegerField(null=True, blank=True, default=0)
    coupon=models.ForeignKey("Coupon", on_delete=models.SET_NULL, null=True, blank=True) 

    def __str__(self):
        return f"Basket - {self.user}"

    def get_total_amount(self):
        """Calculates the total amount considering discounts."""
        total_amount = sum(
            (order.product.price_with_discount if order.product.price_with_discount else order.product.price) * order.count
            for order in self.order_detail.all()
        )
        
        if self.coupon and self.coupon.is_valid():
            discount_price = (self.coupon.discount / 100) * total_amount
            return float(total_amount - discount_price)
        
        self.coupon=None
        self.save(update_fields=['coupon'])
        return total_amount

    def get_free_transportation(self):
        """Returns the remaining amount needed for free shipping."""
        free_threshold = SiteSetting.get_free_shipping_threshold()
        return max(0, free_threshold - self.get_total_amount())

    def get_free_transportation_progress(self):
        """Calculates progress towards free shipping."""
        threshold = SiteSetting.get_free_shipping_threshold()
        total = self.get_total_amount()
        return min((total / threshold) * 100 if threshold else 100, 100)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order_basket = models.ForeignKey(OrderBasket, on_delete=models.CASCADE, related_name='order_detail')
    count = models.PositiveIntegerField()
    final_price = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.order_basket)

    def get_total_price(self):
        """Calculates total price per item considering discounts."""
        return (self.product.price_with_discount or self.product.price) * self.count


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    is_active = models.BooleanField(default=False)

    def is_valid(self):
        """Check if coupon is active and within the valid time range."""
        return self.is_active and self.valid_from <= now() <= self.valid_to

    def __str__(self):
        return self.code










# class OrderBasket(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     is_paid = models.BooleanField(default=False)
#     payment_date = models.DateTimeField(null=True, blank=True)
#     discount = models.PositiveIntegerField(null=True, blank=True, default=0)  # This stores the discount percentage

#     def __str__(self):
#         return f"Basket - {self.user}"

#     def get_total_amount(self):
#         """Calculates the total amount considering discounts (excluding transportation)."""
#         total_amount = sum(
#             (order.product.price_with_discount if order.product.price_with_discount else order.product.price) * order.count
#             for order in self.order_detail.all()
#         )
        
#         if self.discount:
#             discount_price = (self.discount / 100) * total_amount
#             return float(total_amount - discount_price)
        
#         return total_amount

#     def get_free_transportation(self):
#         """Returns the remaining amount needed for free shipping."""
#         free_threshold = SiteSetting.get_free_shipping_threshold()
#         return max(0, free_threshold - self.get_total_amount())

#     def get_free_transportation_progress(self):
#         """Calculates progress towards free shipping."""
#         threshold = SiteSetting.get_free_shipping_threshold()
#         total = self.get_total_amount()
#         return min((total / threshold) * 100 if threshold else 100, 100)



# class OrderBasket(models.Model):
#     user=models.ForeignKey(User,on_delete=models.PROTECT)
#     is_paid=models.BooleanField(default=False)
#     payment_date=models.DateTimeField(null=True,blank=True)
#     discount=models.PositiveIntegerField(null=True,blank=True,default=0)

#     def __str__(self):
#         return str(self.user)
    
    
#     def get_total_amount(self):
#         if self.is_paid:
#             total_amount=0
#             if self.discount:
#                 for order_detail in self.order_detail.all():
#                     total_amount+=order_detail.final_price *order_detail.count
#                 discount_price=(self.discount / 100 )*total_amount
#                 return float(total_amount-discount_price)
            
#             for order_detail in self.order_detail.all():
#                 total_amount+=order_detail.final_price *order_detail.count
#         else:
#             total_amount=0
#             if self.discount:
#                 for order_detail in self.order_detail.all():
#                     if order_detail.product.price_with_discount:
#                         total_amount+=order_detail.product.price_with_discount *order_detail.count
#                     else:
#                         total_amount+=order_detail.product.price *order_detail.count
#                 discount_price=(self.discount / 100 )*total_amount
#                 return float(total_amount-discount_price)
#             for order_detail in self.order_detail.all():
#                 if order_detail.product.price_with_discount:
#                     total_amount+=order_detail.product.price_with_discount *order_detail.count
#                 else:
#                     total_amount+=order_detail.product.price *order_detail.count
                        
#         return total_amount
    
#     def get_free_transportation(self):
#         total = self.get_total_amount()
#         free_threshold = SiteSetting.get_free_shipping_threshold() 
#         return max(0, free_threshold - total)
    
#     def get_free_transportation_progress(self):
#         """Calculates the progress percentage towards free shipping."""
#         threshold = SiteSetting.get_free_shipping_threshold()  # Get dynamic threshold
#         total = self.get_total_amount()  # Get current basket total
        
#         if threshold == 0:  # Prevent division by zero
#             return 100  

#         progress = (total / threshold) * 100
#         return min(progress, 100)  # Ensure it doesn't exceed 100%


# class OrderDetail(models.Model):
#     product=models.ForeignKey(Product,on_delete=models.PROTECT)
#     order_basket=models.ForeignKey(OrderBasket,on_delete=models.CASCADE,related_name='order_detail')
#     count=models.PositiveIntegerField()
#     final_price=models.BigIntegerField(null=True,blank=True)

#     def __str__(self):
#         return str(self.order_basket)
    
#     def get_total_price(self):
#         if self.product.price_with_discount and self.product.discount_percent:
#             return self.product.price_with_discount * self.count
#         return self.product.price * self.count


# class Coupon(models.Model):
#     code=models.CharField(max_length=15,unique=True)
#     valid_from=models.DateTimeField()
#     valid_to=models.DateTimeField()
#     discount=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(99)])
#     is_active=models.BooleanField(default=False)

#     def __str__(self):
#         return self.code