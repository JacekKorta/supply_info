from datetime import datetime

from django.db import models
from django.conf import settings

from supply_info.sp_modules import products_info as pi
from shipments.models import Shipment, ShipmentDetail

class Product(models.Model):
    TYP_CHOICES = pi.TYPE_CATEGORIES
    SUBTYPE_CHOICES = pi.SUBTYPE_CATEGORIES
    code = models.CharField(max_length=60, unique=True, verbose_name='Kod')
    manufacturer = models.CharField(max_length=30, blank=True, null=True, verbose_name='Producent')
    name = models.CharField(max_length=400, verbose_name='Nazwa')
    prod_group = models.CharField(max_length=60, blank=True, null=True)
    type = models.CharField(max_length=30, choices=TYP_CHOICES, default='Akcesoria', blank=True, null=True)
    sub_type = models.CharField(max_length=30,choices=SUBTYPE_CHOICES, default='Inne', blank=True, null=True)
    mark = models.CharField(max_length=3, blank=True, null=True, verbose_name='Znacznik')
    additional_info = models.CharField(max_length=400, blank=True, null=True, verbose_name='Dodatkowe informacje')
    next_shipment = models.DateField(blank=True, null=True, verbose_name='Następna dostawa')
    site_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='link do strony')

    @property
    def get_next_shipment(self):
        today = datetime.today()
        try:
            shipment = Shipment.objects.\
                filter(shipmentdetail__product=self).\
                filter(shipment_status='pending').\
                exclude(estimated_time_arrival__lte=today).\
                order_by('estimated_time_arrival').first()
            return shipment.estimated_time_arrival
        except AttributeError:
            return None

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkty'


class PriceList(models.Model):
    product_code = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="price_lists")
    price_a = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena A')
    price_b = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena B')
    price_c = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena C')
    price_d = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena D')

    def __str__(self):
        return f'{self.product_code}:\n' \
               f'| Cena A: {self.price_a} zł \n' \
               f'| Cena B: {self.price_b} zł \n' \
               f'| Cena C: {self.price_c} zł \n' \
               f'| Cena D: {self.price_d} zł |'

    class Meta:
        verbose_name = 'Ceny'
        verbose_name_plural = 'Ceny'


class ActiveProductList(models.Model):
    product_code = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="active_product_list")
    is_active = models.BooleanField(default=False, verbose_name='Aktywny(zaznaczony)')

    def change_activity(self, new_status):
        self.is_active = new_status
        self.save()

    def __str__(self):
        return f'{self.product_code} status: ACTIVE' if self.is_active is True \
            else f'{self.product_code} status: INACTIVE'

    class Meta:
        verbose_name = 'Aktywność'
        verbose_name_plural = 'Aktywność'


class ProductAvailability(models.Model):
    product_code = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_availability")
    availability = models.IntegerField(verbose_name='Stan magazynowy')
    not_enough = models.IntegerField(default=5, blank=True, null=True, verbose_name='Mało')
    unavailable = models.IntegerField(default=0, blank=True, null=True, verbose_name='Brak')

    @property
    def availability_info(self):
        # values can be different for each product.
        if None not in (self.not_enough, self.unavailable):
            if self.availability >= self.not_enough:
                availability_info = 'Dużo'
            elif self.availability > self.unavailable:
                availability_info = 'Mało'
            else:
                availability_info = 'Brak'
            return availability_info

    def __str__(self):
        return f'{self.availability}'

    class Meta:
        verbose_name = 'Informacje o dostępności'
        verbose_name_plural = 'Informacje o dostępności'


class Event(models.Model):
    user_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Użytkownik')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Data')
    event_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Zdarzenie')

    class Meta:
        verbose_name = 'Zdarzenie'
        verbose_name_plural = 'Zdarzenia'


class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Użytkownik')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Produkt')
    less_or_equal = models.BooleanField(default=True,
                                        help_text='If True, then alert will appear when the product quantity'
                                                  ' will be less or equal than qty_lvl', verbose_name='Mniej/więcej')
    qty_alert_lvl = models.PositiveSmallIntegerField(verbose_name='Poziom alertu')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    updated = models.DateTimeField(auto_now=True, verbose_name='Edytowano')
    is_active = models.BooleanField(default=True, verbose_name='Aktywny')

    def __str__(self):
        return f'Alert utworzony przez {self.user.username} na produkt {self.product.code} na poziomie {self.qty_alert_lvl}'

    class Meta:
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerty'