from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from supply_info.models import Alert, Product


class BasicSetup(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            type='maszyny',
            mark='M',
            availability=10,
            is_active=True
        )
        Product.objects.create(
            code='Machine2',
            name='machine_2 desc',
            type='maszyny',
            mark='M',
            availability=0,
            is_active=True
        )
        Alert.objects.create(user=self.user,
                             product=Product.objects.get(code='Machine1'),
                             qty_alert_lvl=10
                             )
        Alert.objects.create(user=self.user,
                             product=Product.objects.get(code='Machine2'),
                             less_or_equal=False,
                             qty_alert_lvl=4
                             )


class LoggedInTestCase(BasicSetup):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')
        return super().setUp()


