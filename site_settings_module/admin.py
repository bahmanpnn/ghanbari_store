from django.contrib import admin
from .models import SiteSetting,BranchLocation


admin.site.register(SiteSetting)
admin.site.register(BranchLocation)