from django.db import models
from django.utils import timezone


class Product(models.Model):
    code = models.CharField(max_length=60)
    manufacturer = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=30)
    sub_type = models.CharField(max_length=30)
    mark = models.CharField(max_length=3)
    price_a = models.DecimalField(max_digits=15, decimal_places=2)
    price_b = models.DecimalField(max_digits=15, decimal_places=2)
    price_c = models.DecimalField(max_digits=15, decimal_places=2)
    price_d = models.DecimalField(max_digits=15, decimal_places=2)
    availability = models.IntegerField
    is_active = models.BooleanField(default=False)

    def change_activity(self, new_status):
        self.is_active = new_status
        self.save()

    def __str__(self):
        return self.code
