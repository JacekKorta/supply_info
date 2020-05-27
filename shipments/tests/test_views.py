from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .setUp import BasicSetup, StaffUserLoggedInTestCase, AdminLoggedInTestCase, LoggedInTestCase
from supply_info.models import Product


class BasicViewsTest(BasicSetup):

    def test_the_nearest_shipment_is_visible_in_next_shipment_field(self):
        self.expected_eta = datetime.now().date() + timedelta(days=120)
        response = self.client.get(reverse('supply_info:machines_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Machine1')
        self.assertContains(response, 'Machine2')
        self.assertContains(response, self.expected_eta.day)
        self.assertContains(response, self.expected_eta.year)


class StaffUserLoggedInTests(StaffUserLoggedInTestCase):
    def test_shipment_menu_is_visible(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertContains(response, 'dostawy maszyn')
        self.assertContains(response, 'dodaj dostawę')

    def test_all_machines_are_visible(self):
        machines = Product.objects.filter(mark='M').order_by("code")
        response = self.client.get(reverse('shipments:shipments_view'))
        for machine in machines:
            self.assertContains(response, machine)

    def test_future_shipment_is_visible(self):
        response = self.client.get(reverse('shipments:shipments_view'))
        self.assertContains(response, 'TW0001')

    def test_past_shipment_is_not_visible(self):
        response = self.client.get(reverse('shipments:shipments_view'))
        self.assertNotContains(response, 'TH0001')

    def test_shipment_detail_site_works(self):
        response = self.client.get(reverse('shipments:shipments_details', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_shipment_detail_site_has_full_info(self):
        response = self.client.get(reverse('shipments:shipments_details', kwargs={'pk':1}))
        self.assertContains(response, 'TW0001')
        self.assertContains(response, 'Machine1')
        self.assertContains(response, 'Machine2')
        self.assertContains(response, '50')
        self.assertContains(response, '120')
        self.assertContains(response, 'Drukuj')


class UserLoggedIn(LoggedInTestCase):
    def test_shipment_menu_is_Notvisible(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertNotContains(response, 'dostawy maszyn')
        self.assertNotContains(response, 'dodaj dostawę')

    def test_shipment_site_is_not_visible(self):
        response = self.client.get(reverse('shipments:shipments_view'))
        self.assertNotEqual(response.status_code, 200)