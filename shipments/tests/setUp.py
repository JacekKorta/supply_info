from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from shipments.models import Shipment, ShipmentDetail
from supply_info.models import Product


class BasicSetup(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            type='maszyny',
            mark='M',
            is_active=True,
            availability=10
        )
        Product.objects.create(
            code='Machine2',
            name='machine_2 desc',
            type='maszyny',
            mark='M',
            is_active=True,
            availability=0
        )

        # future shipment
        Shipment.objects.create(
            shipment_number='TW0001',
            shipment_status='new',
            country_of_origin='oth',
            created=datetime.now().date(),
            estimated_time_arrival=datetime.now().date() + timedelta(days=10)
        )
        ShipmentDetail.objects.create(
            shipment=Shipment.objects.get(pk=1),
            product=Product.objects.get(pk=1),
            quantity=50,
        )
        ShipmentDetail.objects.create(
            shipment=Shipment.objects.get(pk=1),
            product=Product.objects.get(pk=2),
            quantity=120,
        )
        # second shipment
        Shipment.objects.create(
            shipment_number='TW0002',
            shipment_status='pending',
            country_of_origin='oth',
            created=datetime.now().date(),
        )
        ShipmentDetail.objects.create(
            shipment=Shipment.objects.get(pk=2),
            product=Product.objects.get(pk=1),
            quantity=30,
        )

        # third, past shipment
        Shipment.objects.create(
            shipment_number='TH0001',
            shipment_status='pending',
            country_of_origin='oth',
            created=datetime.now().date(),
            estimated_time_arrival = datetime.now().date() - timedelta(days=1),
        )
        ShipmentDetail.objects.create(
            shipment=Shipment.objects.get(pk=3),
            product=Product.objects.get(pk=2),
            quantity=10,
        )

class LoggedInTestCase(BasicSetup):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')
        return super().setUp()


class AdminLoggedInTestCase(BasicSetup):
    def setUp(self):
        self.user = User.objects.create_superuser('Artur_admin', 'artur_the_admin@example.com', 'arturadminpassword')
        self.client.login(username='Artur_admin', password='arturadminpassword')
        return super().setUp()


class StaffUserLoggedInTestCase(BasicSetup):
    def setUp(self):
        self.user = User.objects.create_user('adam', email='adam@example.com', password='adampassword', is_staff=True)
        self.client.login(username='adam', password='adampassword')
        return super().setUp()