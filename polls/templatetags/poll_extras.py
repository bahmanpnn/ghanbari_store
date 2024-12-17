from django import template
# from jalali_date import date2jalali,datetime2jalali

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


# @register.filter(name='jalal_date')
# def jalal_date(value):
#     # print(value)
#     return datetime2jalali(value)

# @register.filter(name='jalal_time')
# def jalal_time(value):
#     return date2jalali(value)
    