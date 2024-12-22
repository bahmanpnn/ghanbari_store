from django.db import models
from account_module.models import User
from django.utils.text import slugify


class Article(models.Model):
    title=models.CharField(max_length=255,db_index=True,unique=True,null=True,blank=True)
    short_description=models.TextField(max_length=510)
    text=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='images/blog/articles')
    created_date=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(blank=True,unique=True,null=True,db_index=True,allow_unicode=True,max_length=127)
    author=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        
        self.slug=slugify(self.title,allow_unicode=True)
        return super().save(*args, **kwargs)

# class ArticleImages(models.Model):
#     pass

# class ArticleComment(models.Model):
#     pass