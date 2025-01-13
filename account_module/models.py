from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):
    phone_number=models.CharField(max_length=11,unique=True,null=True,blank=False)
    email_active_code=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to='images/authors',null=True,blank=True)
    
    # USERNAME_FIELD='phone_number' 
    # REQUIRED_FIELDS=[]

    def __str__(self):
        if self.email:
            return self.email
        elif self.phone_number:
            return self.phone_number
        
        return self.username
        # return '' or None
        
        
class UserAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_address')
    province=models.CharField(max_length=63)
    city=models.CharField(max_length=63)
    main_address=models.TextField()

    def __str__(self):
        return f'{self.province} - {self.city} - {self.main_address} - {self.user}'
    

class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999)).zfill(6)
        self.save()
