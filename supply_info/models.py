from datetime import datetime

from django.db import models
from django.conf import settings
from django.shortcuts import reverse

from supply_info.sp_modules import products_info as pi
from shipments.models import Shipment


class Product(models.Model):
    TYP_CHOICES = pi.TYPE_CATEGORIES
    SUBTYPE_CHOICES = pi.SUBTYPE_CATEGORIES
    code = models.CharField(max_length=60, unique=True, verbose_name='Kod')
    manufacturer = models.CharField(max_length=30, blank=True, null=True, verbose_name='Producent')
    name = models.CharField(max_length=800, verbose_name='Nazwa')
    prod_group = models.CharField(max_length=60, blank=True, null=True)
    type = models.CharField(max_length=30, choices=TYP_CHOICES, default='Akcesoria', blank=True, null=True)
    sub_type = models.CharField(max_length=30, choices=SUBTYPE_CHOICES, default='Inne', blank=True, null=True)
    mark = models.CharField(max_length=3, blank=True, null=True, verbose_name='Znacznik')
    additional_info = models.CharField(max_length=800, blank=True, null=True, verbose_name='Dodatkowe informacje')
    next_shipment = models.DateField(blank=True, null=True, verbose_name='Następna dostawa')
    site_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='link do strony')

    # availability
    availability = models.IntegerField(verbose_name='Stan magazynowy', default=0)
    not_enough = models.IntegerField(default=5, blank=True, null=True, verbose_name='Mało')
    unavailable = models.IntegerField(default=0, blank=True, null=True, verbose_name='Brak')
    is_active = models.BooleanField(default=False, verbose_name='Aktywny', help_text="Działa gdy zaznaczony")
    synchronize = models.BooleanField(default=True, verbose_name='Synchronizuj', help_text="Działa gdy zaznaczony")

    # prices
    price_a = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Cena A')
    price_b = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Cena B')
    price_c = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Cena C')
    price_d = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Cena D')

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
        return self.code

    def change_activity(self, new_status):
        self.is_active = new_status
        self.save()

    def change_synchronize(self, new_status):
        self.synchronize = new_status
        self.save()

    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkty'


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
    qty_alert_lvl = models.PositiveSmallIntegerField(verbose_name='Poziom alertu (szt.)')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    updated = models.DateTimeField(auto_now=True, verbose_name='Edytowano')
    is_active = models.BooleanField(default=True, verbose_name='Aktywny')

    def get_absolute_url(self):
        return reverse('supply_info:alert_edit_view', args=[self.id])

    def __str__(self):
        return f'Alert utworzony przez {self.user.username} na produkt {self.product.code} na poziomie {self.qty_alert_lvl}'

    class Meta:
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerty'