from django import template
from ..models import Product, PriceList, ProductAvailability, ActiveProductList


register = template.Library()


@register.filter
def my_filter(products, category):
    return products.filter(sub_type=category).order_by("code")