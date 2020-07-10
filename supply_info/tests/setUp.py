from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from supply_info.models import Alert, Product, ProductAvailability, ActiveProductList


class BasicSetup(TestCase):
    def setUp(self):
        p = Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            type='maszyny',
            mark='M'
        )
        p.save()
        a = ProductAvailability(product_code=Product.objects.get(code="Machine1"), availability=10)
        a.save()
        a = ActiveProductList(product_code=Product.objects.get(code="Machine1"))
        a.is_active = True
        a.save()
        Product.objects.create(
            code='Machine2',
            name='machine_2 desc',
            type='maszyny',
            mark='M'
        )
        b = ProductAvailability(product_code=Product.objects.get(code="Machine2"), availability=0)
        b.save()
        b = ActiveProductList(product_code=Product.objects.get(code="Machine2"))
        b.is_active = True
        b.save()
        Alert(user=self.user,
              product=Product.objects.get(code='Machine1'),
              qty_alert_lvl=10
              )
        Alert(user=self.user,
              product=Product.objects.get(code='Machine2'),
              less_or_equal=False,
              qty_alert_lvl=4
              )


class LoggedInTestCase(BasicSetup):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')
        return super().setUp()
