from django.contrib import admin
from .models import ActiveProductList, PriceList, Product

admin.site.register(PriceList)
admin.site.register(Product)
admin.site.register(ActiveProductList)