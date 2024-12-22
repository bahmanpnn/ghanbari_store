from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number=models.CharField(max_length=11,unique=True,null=True,blank=False)
    email_active_code=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to='images/auhtors',null=True,blank=True)
    
    # USERNAME_FIELD='phone_number' 
    # REQUIRED_FIELDS=[]

    def __str__(self):
        if self.email:
            return self.email
        elif self.phone_number:
            return self.phone_number
    