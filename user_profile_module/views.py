from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.db.models import Count
from order_module.models import OrderBasket
from account_module.models import User
# from .forms import EditUserForm,EditUserAddressForm,ChangePasswordForm
from .models import UserFavoriteProduct
# from permissions import is_authenticated_permission
from django.utils.decorators import method_decorator


# @method_decorator(is_authenticated_permission,name='dispatch')
class UserProfileView(View):
    template_name='user_profile_module/user_profile.html'
    
    def get(self,request):
        user_orders=OrderBasket.objects.annotate(items=Count('order_detail')).filter(is_paid=True,user_id=request.user.id)
        return render(request,self.template_name,{
            'user_orders':user_orders
        })


# @is_authenticated_permission
def user_favorite_products(request):
    user_favorite_products=UserFavoriteProduct.objects.filter(user_id=request.user.id).order_by('product__added_date')

    return render(request,'user_profile_module/user_favorites.html',{
        'user_favorite_products':user_favorite_products
    })