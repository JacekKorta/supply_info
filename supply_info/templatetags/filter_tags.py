from django import template
from ..models import Product, PriceList, ProductAvailability, ActiveProductList


register = template.Library()


@register.filter
def my_filter(products, sub_type):
    return products.filter(sub_type=sub_type).order_by("code")