from .models import OrderBasket
from site_settings_module.models import SiteSetting


def basket_products(request):
    user_basket=OrderBasket.objects.prefetch_related('order_detail').filter(is_paid=False,user_id=request.user.id).first()
    
    if user_basket is not None:
        context={
            'user_basket':user_basket,
            'need_for_free_transportation': SiteSetting.get_free_shipping_threshold(),
            'transportation_rate': SiteSetting.get_transportation_rate(),
        }
        return context
    else:
        return {'user_basket':None}
