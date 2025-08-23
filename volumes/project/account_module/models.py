from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
import random


class User(AbstractUser):
    phone_number=models.CharField(max_length=11,unique=True,null=True,blank=False)
    image=models.ImageField(upload_to='images/authors',null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    
    # USERNAME_FIELD='phone_number' 
    # REQUIRED_FIELDS=[]

    def __str__(self):
        if self.email:
            return f'{self.email} - {self.phone_number}'
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
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)
    # otp = models.CharField(max_length=6, default=lambda: str(random.randint(100000, 999999)), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self, expiration_minutes=15):
        """
        Checks if the OTP is still valid.
        :param expiration_minutes: OTP validity duration in minutes.
        """
        return now() <= self.created_at + timedelta(minutes=expiration_minutes)

    def generate_otp(self, save=True):
        """
        Generates a 6-digit OTP and optionally saves it to the database.
        :param save: If True, saves the OTP to the database.
        """
        self.otp = str(random.randint(100000, 999999)).zfill(6)
        self.created_at=now()
        if save:
            self.save()

    def __str__(self):
        return f"OTP for {self.user.phone_number} (valid until {self.created_at + timedelta(minutes=15)})"
  
    # def send_otp(phone_number, otp):
    #     # todo:send otp code with sms provider or seprate send otp and make it in utils services
    #     print(f"Sending OTP {otp} to {phone_number}") 

