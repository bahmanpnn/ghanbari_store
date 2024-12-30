from django import template
from jalali_date import date2jalali,datetime2jalali
# import pytz
# from django.utils.timezone import make_aware


register=template.Library()


@register.filter(name='three_digits')
def three_digits(value:int):
    return '{:,}'.format(value)

# @register.simple_tag
# def multiply(price,count,*args, **kwargs):
#     return three_digits(price*count)

# @register.simple_tag
# def tax(total_amount):
#     return three_digits(total_amount/10)



@register.filter(name='jalal_date')
def jalal_date(value):
    
    # # Ensure the value is timezone-aware
    # if not value.tzinfo:
    #     value = make_aware(value)
    
    # Convert the time to Iran's timezone
    # iran_tz = pytz.timezone('Asia/Tehran')
    # local_value = value.astimezone(iran_tz)

    return datetime2jalali(value).strftime('%H:%M:%S - %y/%m/%d ')

@register.filter(name='jalal_time')
def jalal_time(value):
    return date2jalali(value)

