from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductCommentReview,CommentReviewStatusType


@receiver(post_save, sender=ProductCommentReview)
def update_product_avg_rating_on_acceptance(sender, instance, **kwargs):
    """
    Update the product's avg_rate only when a review is marked as accepted by admin in admin panel.
    """
    if instance.status == CommentReviewStatusType.accepted.value:
        product = instance.product
        product.avg_rate = product.productcommentreview_set.filter(
            status=CommentReviewStatusType.accepted.value
        ).aggregate(Avg('rating'))['rating__avg'] or 0
        product.save(update_fields=['avg_rate'])