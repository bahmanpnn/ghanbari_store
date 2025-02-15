from django.shortcuts import render
from django.views import View
from account_module.models import User
from order_module.models import OrderBasket
from django.db.models import Sum, F, ExpressionWrapper, FloatField


class AboutUsView(View):
    template_name = "about_us_module/about_us.html"

    def get(self, request):
        # Aggregate total orders and total paid amount
        stats = OrderBasket.objects.filter(is_paid=True).aggregate(
            total_orders=Sum(1),  # Counting all paid orders
            total_paid_amount=Sum(
                ExpressionWrapper(
                    F("order_detail__final_price") * F("order_detail__count"),
                    output_field=FloatField()
                )
            )
        )

        # Prepare context with safe defaults (avoiding None)
        context = {
            'user_count': User.objects.count(),  # More efficient
            "total_orders": stats["total_orders"] or 0,  
            "total_paid_amount": stats["total_paid_amount"] or 0,  
        }
        return render(request, self.template_name, context)



# class AboutUsView(View):
#     template_name="about_us_module/about_us.html"

#     def get(self,request):

#         # Get total paid orders count
#         total_paid_orders = OrderBasket.objects.filter(is_paid=True).count()

#         # Get total paid amount considering discounts
#         total_paid_amount = (
#             OrderBasket.objects.filter(is_paid=True)
#             .annotate(
#                 total_price=Sum(F("order_detail__final_price") * F("order_detail__count")),
#                 discount_amount=ExpressionWrapper(
#                     (F("discount") / 100.0) * F("total_price"),
#                     output_field=FloatField(),
#                 )
#             )
#             .aggregate(total_amount=Sum(F("total_price") - F("discount_amount")))
#         )


#         context={
#             'user_count':User.objects.all().count(),
#             'total_paid_orders':total_paid_orders,
#             'total_paid_amount':total_paid_amount["total_amount"] or 0,

#         }
#         return render(request,self.template_name,context)
