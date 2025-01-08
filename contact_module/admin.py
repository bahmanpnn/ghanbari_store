from django.contrib import admin
from .models import ContactModel,ContactSubjectItem

admin.site.register(ContactModel)
admin.site.register(ContactSubjectItem)