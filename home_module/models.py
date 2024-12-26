from django.db import models
from django.urls import reverse


class Slider(models.Model):
    title=models.CharField(max_length=100)
    # text=RichTextField(config_name='default')  # Specify the config if needed
    text=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    image=models.ImageField(upload_to='sliders/',null=True)
    link_url=models.URLField(null=True,blank=True)
    btn_text=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.title