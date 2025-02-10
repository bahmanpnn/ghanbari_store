from django.contrib import admin
from .models import Product,ProductImage,ProductOfTheWeek,ProductCommentReview, CommentReviewStatusType



class ProductAdmin(admin.ModelAdmin):
    list_display=['title','slug','price','is_active','price_with_discount','avg_rate']


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductOfTheWeek)


@admin.register(ProductCommentReview)
class ProductCommentReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'status', 'created_date')
    list_filter = ('status',)
    actions = ['approve_reviews']

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        queryset.update(status=CommentReviewStatusType.accepted.value)
        for review in queryset:
            review.save()  # This triggers the signal to update avg_rate
