from django.conf import settings
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=56, unique=True, verbose_name='Kod')
    tax_number = models.CharField(max_length=30, unique=True, blank=True, null=True, verbose_name='NIP/Vies')
    email = models.EmailField(null=True, blank=True)
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienci'


class Machine(models.Model):
    code = models.CharField(max_length=50, verbose_name='Nazwa')
    serial_number = models.CharField(max_length=12, unique=True, verbose_name='Numer seryjny')
    delivery_date = models.DateField(verbose_name='Data przypłynięcia', blank=True, null=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Maszyna'
        verbose_name_plural = 'Maszyny'


class ShipmentToCustomer(models.Model):
    delivery_note_number = models.CharField(max_length=20, verbose_name='WZ')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Klient')
    item = models.ForeignKey('Machine', on_delete=models.CASCADE, verbose_name='Maszyna')
    shipment_date = models.DateTimeField(auto_now_add=True, verbose_name='Data wysłki')

    def __str__(self):
        return self.delivery_note_number

    class Meta:
        verbose_name = 'Dokument WZ'
        verbose_name_plural = 'Dokument WZ'