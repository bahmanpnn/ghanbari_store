from django.contrib import admin
from .models import Article,ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    list_display=['title','author','is_active']
    list_filter=['is_active','author','created_date']

    def save_model(self, request, obj, form, change):
        # print(change)
        # print(form)
        # print(request.user)
        if not change:
            obj.author=request.user
        return super().save_model(request, obj, form, change)
    

admin.site.register(Article,ArticleAdmin)
admin.site.register(ArticleComment)