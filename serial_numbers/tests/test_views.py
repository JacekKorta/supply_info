from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')


class AdminLoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('Artur_admin', 'artur_the_admin@example.com', 'arturadminpassword')
        self.client.login(username='Artur_admin', password='arturadminpassword')


class TestPageAdminLogged(AdminLoggedInTestCase):
    def test_register_machines_page_works(self):
        response = self.client.get(reverse('serial_numbers:register_machines_in_warehouse'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'serial_numbers/register_machines.html')
        self.assertContains(response, 'Zarejestruj maszyny w magazynie')
        self.assertContains(response, 'Administracja')
        self.assertContains(response, 'Magazyn')

    def test_save_shipment_page_works(self):
        current_year = datetime.now().year
        response = self.client.get(reverse('serial_numbers:save_shipment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'serial_numbers/add_shipment.html')
        self.assertContains(response, 'Dodaj wysyłkę')
        self.assertContains(response, 'Administracja')
        self.assertContains(response, 'Magazyn')
        self.assertContains(response, 'Klient:')
        self.assertContains(response, 'Dokument:')
        self.assertContains(response, 'WZ/')
        self.assertContains(response, f'{current_year}')
        self.assertContains(response, 'Numery seryjne:')


class TestPageLogged(LoggedInTestCase):
    def test_register_machines_page_works(self):
        response = self.client.get(reverse('serial_numbers:register_machines_in_warehouse'))
        self.assertEqual(response.status_code, 302)

    def test_save_shipment_page_works(self):
        response = self.client.get(reverse('serial_numbers:save_shipment'))
        self.assertEqual(response.status_code, 302)


class TestPageAnonymous(TestCase):
    def test_register_machines_page_works(self):
        response = self.client.get(reverse('serial_numbers:register_machines_in_warehouse'))
        self.assertEqual(response.status_code, 302)

    def test_save_shipment_page_works(self):
        response = self.client.get(reverse('serial_numbers:save_shipment'))
        self.assertEqual(response.status_code, 302)

