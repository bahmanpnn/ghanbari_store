from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number=models.CharField(max_length=11,unique=True,null=True,blank=True)
    email_active_code=models.CharField(max_length=100,null=True)
    
    def __str__(self):
        if self.username:
            return self.username
        return self.email
    