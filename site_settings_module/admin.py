from django.contrib import admin
from .models import SiteSetting,BranchLocation,FooterLinkBox,FooterLinkItem,SiteBanner,TeamMember


admin.site.register(SiteSetting)
admin.site.register(BranchLocation)
admin.site.register(FooterLinkBox)
admin.site.register(FooterLinkItem)
admin.site.register(SiteBanner)
admin.site.register(TeamMember)