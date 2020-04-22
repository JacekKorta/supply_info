from django.db import models
from serial_numbers.models import Customer
from supply_info.models import Product


class Order(models.Model):
    ORDERS_STATUS = (
        ('new', 'Nowe'),
        ('accepted', 'Przyjęte'),
        ('canceled', 'Anulowane'),
        ('partial', 'Zrealizowane częściowo'),
        ('done', 'Zrealizowane')
    )
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Klient')
    order_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Nr proformy')
    order_date = models.DateField(verbose_name='Data zamówienia')
    order_status = models.TextField(choices=ORDERS_STATUS, verbose_name='Status zamówienia', default='new')
    sell_date = models.DateField(verbose_name='Data sprzedaży', blank=True, null=True)

    def __str__(self):
        return f'Zamówienie {self.order_number} dla {self.customer_id} z dnie {self.order_date}'

    class Meta:
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamówienia'


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Zamówienie')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produkt')
    quantity = models.IntegerField(verbose_name='Ilosć')

    class Meta:
        verbose_name = 'Szczegóły zamówienia'
        verbose_name_plural = 'Szczegóły zamówień'
