from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from supply_info.models import Alert, Product, ProductAvailability, ActiveProductList
from .setUp import BasicSetup, LoggedInTestCase


class BasicViewTest(LoggedInTestCase):

    def test_alert_list_page_works(self):
        response = self.client.get(reverse('supply_info:alerts_list_view'))
        self.assertEqual(response.status_code, 200)

    def test_alerts_are_visible_on_the_list(self):
        response = self.client.get(reverse('supply_info:alerts_list_view'))
        self.assertContains(response, 'Machine1')
        self.assertContains(response, '10')
        self.assertContains(response, 'mniej lub równe')
        self.assertContains(response, 'Machine2')
        self.assertContains(response, '4')
        self.assertContains(response, 'więcej niż')