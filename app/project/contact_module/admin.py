from django.contrib import admin
from .models import ContactModel,ContactSubjectItem,UserEmailForNews

admin.site.register(ContactModel)
admin.site.register(ContactSubjectItem)
admin.site.register(UserEmailForNews)