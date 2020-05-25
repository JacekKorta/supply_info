from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .setUp import BasicSetup, StaffUserLoggedInTestCase, AdminLoggedInTestCase, LoggedInTestCase
from supply_info.models import Product


class BasicFormTest(StaffUserLoggedInTestCase):

    @property
    def response(self):
        return self.client.get(reverse('shipments:add_new_shipment'))

    def test_order_form_respond(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_includes_all_machines(self):
        machines = Product.objects.filter(mark='M').order_by("code")
        for machine in machines:
            self.assertContains(self.response, machine)

