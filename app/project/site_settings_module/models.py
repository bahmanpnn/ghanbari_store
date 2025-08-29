from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
# from ckeditor.fields import CKEditor5Field 


class SiteSetting(models.Model):
    site_logo=models.ImageField(upload_to='images/site_logo/',blank=True,null=True)
    is_main_setting=models.BooleanField(default=True)
    phone=models.CharField(max_length=31,blank=True,null=True)
    email=models.EmailField(max_length=31,blank=True,null=True)
    copy_right=CKEditor5Field(blank=True,null=True)
    about_us=CKEditor5Field('Text', config_name='default',blank=True,null=True)
    site_name=models.CharField(max_length=150)
    site_url=models.CharField(max_length=255)

    # #social media
    # facebook=models.URLField(blank=True,null=True)
    # whatsup=models.URLField(blank=True,null=True)
    # instagram=models.URLField(blank=True,null=True)
    # telegram=models.URLField(blank=True,null=True)
    # twitter=models.URLField(blank=True,null=True)
    # youtube=models.URLField(blank=True,null=True)

    # free shipping threshold
    free_shipping_threshold = models.PositiveIntegerField(default=150)

    # free shipping threshold
    transportation_rate = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        if SiteSetting.objects.exists() and not self.pk:
            raise ValidationError("فقط یک مقدار تنظیمات مجاز است. ابتدا مقدار قبلی را حذف کنید.")
        super().save(*args, **kwargs)

    @classmethod
    def get_free_shipping_threshold(cls):
        setting = cls.objects.first()
        return setting.free_shipping_threshold if setting else 150

    @classmethod
    def get_transportation_rate(cls):
        setting = cls.objects.first()
        return setting.transportation_rate if setting else 100


class BranchLocation(models.Model):
    branch_name=models.CharField(max_length=127,null=True,blank=False)
    branch_address=models.CharField(max_length=511,null=True,blank=False)
    branch_phone=models.CharField(max_length=63,null=True,blank=True)
    site_setting=models.ForeignKey(SiteSetting,on_delete=models.CASCADE,null=True,blank=False,related_name='branches')


    def __str__(self):
        return f'{self.branch_name} '


class FooterLinkBox(models.Model):
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title    


class FooterLinkItem(models.Model):
    title=models.CharField(max_length=150)
    url_title=models.URLField(max_length=200)
    parent=models.ForeignKey(FooterLinkBox,on_delete=models.CASCADE,related_name='footer_link_items')


    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        article_detail='article_detail','صفحه جزئیات مقالات'
        articles='articles','صفحه مقالات'
        profile_dashboard='profile_dashboard','صفحه پروفایل کاربر (داشبورد)'

    title=models.CharField(max_length=200,null=True,blank=True)
    description=models.CharField(max_length=62,default="")
    url=models.URLField(max_length=400,blank=True,null=True)
    btn_text=models.CharField(max_length=20,null=True,blank=True)
    image=models.ImageField(upload_to='images/banners',null=True,blank=True)
    is_active=models.BooleanField(default=True)

    position=models.CharField(max_length=150,choices=SiteBannerPosition.choices)

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    image=models.ImageField(upload_to='images/team_members',blank=True,null=True)
    full_name=models.CharField(max_length=127)
    position=models.CharField(max_length=127)


class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("whatsup", "Whatsup"),
        ("telegram", "Telegram"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("github", "GitHub"),
    ]

    platform = models.CharField(
        max_length=50, choices=PLATFORM_CHOICES, unique=True
    )
    url = models.URLField()

    def __str__(self):
        return self.get_platform_display()  # Shows the readable name in the admin panel
    



