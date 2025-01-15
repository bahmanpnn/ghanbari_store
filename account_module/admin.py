from django.contrib import admin
from .models import User,UserAddress


class UserAdmin(admin.ModelAdmin):
    list_display=['username','phone_number','email','is_verified']


admin.site.register(User,UserAdmin)
admin.site.register(UserAddress)