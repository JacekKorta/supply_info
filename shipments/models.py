from django.db import models
from datetime import datetime, timedelta


class Shipment(models.Model):
    SHIPMENT_STATUS_CHOICES = (
        ('canceled', 'Anulowane'),
        ('done', 'Dostarczone'),
        ('draft', 'Draft'),
        ('new', 'Nowe'),
        ('pending', 'Oczekujące'),
    )
    COUNTRY_CHOICES =(
        ('rt', 'Holandia'),
        ('yp', 'Japonia'),
        ('pl', 'Polska'),
        ('th', 'Tajlandia'),
        ('tw', 'Tajwan'),
        ('oth', 'Inne'),
    )

    def default_eta():
        # usually the eta is about 3-4 month after order was placed
        today = datetime.now().date()
        return today + timedelta(days=120)

    estimated_time_arrival = models.DateField(verbose_name='ETA', default=default_eta())
    shipment_number = models.CharField(max_length=10, verbose_name='Numer dostawy')
    shipment_status = models.CharField(max_length=12,
                                       choices=SHIPMENT_STATUS_CHOICES,
                                       verbose_name='Status',
                                       default='draft')
    country_of_origin = models.CharField(max_length=9, choices=COUNTRY_CHOICES, verbose_name='Kraj pochodzenia')
    created = models.DateTimeField(verbose_name='Data utworzenia', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Ostatnia aktualizacja', auto_now=True)

    def __str__(self):
        return f'Dostawa {self.shipment_number} z: {self.get_country_of_origin_display()}.' \
               f' Planowana na {self.estimated_time_arrival} - [{self.get_shipment_status_display()}]'

    class Meta:
        verbose_name = 'Dostawa'
        verbose_name_plural = 'Dostawy'


class ShipmentDetail(models.Model):
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE, verbose_name='Dostawa')
    product = models.ForeignKey('supply_info.Product', on_delete=models.CASCADE, verbose_name='Produkt')
    quantity = models.IntegerField(verbose_name='Ilość')

    class Meta:
        verbose_name = 'towar z dostawy'
        verbose_name_plural = 'towary z dostawy'

    def __str__(self):
        return f'Dostawa {self.product} w ilości {self.quantity}'