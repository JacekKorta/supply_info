from django.contrib.auth.models import User
from django.test import TestCase

from supply_info.management.commands.alerts_notifications import Command
from supply_info.models import Alert, Product, ProductAvailability


class NotificationsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')

        Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            type='maszyny',
            mark='M'
        )
        ProductAvailability.objects.create(product_code=Product.objects.get(code="Machine1"), availability=9)

        Product.objects.create(
            code='Machine2',
            name='machine_2 desc',
            type='maszyny',
            mark='M'
        )
        b = ProductAvailability(product_code=Product.objects.get(code="Machine2"), availability=5)
        b.save()

        Alert.objects.create(user=self.user,
                             product=Product.objects.get(code='Machine1'),
                             qty_alert_lvl=10
                             )
        Alert.objects.create(user=self.user,
                             product=Product.objects.get(code='Machine2'),
                             less_or_equal=False,
                             qty_alert_lvl=4
                             )
        Alert.objects.create(user=self.user,
                             product=Product.objects.get(code='Machine2'),
                             less_or_equal=False,
                             qty_alert_lvl=4,
                             is_active=False
                             )
        return super().setUp()

    def test_get_users_pk_method(self):
        users_pk = Command.get_users_pk()
        self.assertEqual(len(users_pk), 1)

    def test_get_user_alerts(self):
        users_pk = Command.get_users_pk()
        users_alerts = Command.get_user_alerts(users_pk[0])
        self.assertTrue(isinstance(users_alerts[0], Alert))
        for alert in users_alerts:
            self.assertEqual(alert.is_active, True)
        self.assertEqual(len(users_alerts), 2)

    def test_alert_check_status(self):
        users_pk = Command.get_users_pk()
        users_alerts = Command.get_user_alerts(users_pk[0])
        alerts_to_send = Command.alerts_to_send(users_alerts)
        self.assertTrue(isinstance(alerts_to_send[0], Alert))
        self.assertEqual(len(alerts_to_send), 2)
