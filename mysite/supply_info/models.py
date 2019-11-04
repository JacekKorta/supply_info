from django.db import models
from django.utils import timezone


class Product(models.Model):
    code = models.CharField(max_length=60, unique=True)
    manufacturer = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    prod_group = models.CharField(max_length=60)
    type = models.CharField(max_length=30)
    sub_type = models.CharField(max_length=30)
    mark = models.CharField(max_length=3)

    def __str__(self):
        return self.code


class PriceList(models.Model):
    product_code = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="price_lists")
    price_a = models.DecimalField(max_digits=10, decimal_places=2)
    price_b = models.DecimalField(max_digits=10, decimal_places=2)
    price_c = models.DecimalField(max_digits=10, decimal_places=2)
    price_d = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product_code}:\n' \
               f'| Cena A: {self.price_a} zł \n' \
               f'| Cena B: {self.price_b} zł \n' \
               f'| Cena C: {self.price_c} zł \n' \
               f'| Cena D: {self.price_d} zł |'


class ActiveProductList(models.Model):
    product_code = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="active_product_list")
    is_active = models.BooleanField(default=False)

    def change_activity(self, new_status):
        self.is_active = new_status
        self.save()

    def __str__(self):
        return f'{self.product_code} status: ACTIVE' if self.is_active is True \
            else f'{self.product_code} status: INACTIVE'


class ProductAvailability(models.Model):
    product_code = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_availability")
    availability = models.IntegerField()
    not_enough = models.IntegerField()
    unavailable = models.IntegerField()

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
        return f'{self.product_code} : {self.availability} sztuk. Stan: {self.availability_info}'
