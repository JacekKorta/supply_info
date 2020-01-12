from django.db import models
from django.utils import timezone

from .sp_modules import products_info as pi


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