import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from supply_info.models import Product


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')


class AdminLoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('Artur_admin', 'artur_the_admin@example.com', 'arturadminpassword')
        self.client.login(username='Artur_admin', password='arturadminpassword')


class TestPageAdminLogged(AdminLoggedInTestCase):
    def test_machines_list_page_works(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/machines_list.html')
        self.assertContains(response, 'Kod produktu')
        self.assertContains(response, 'Stan')
        self.assertContains(response, 'Szukaj')
        self.assertContains(response, 'Lista maszyn')
        self.assertContains(response, 'Admin panel')


class TestPageLogged(LoggedInTestCase):
    def test_machines_list_page_works(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/machines_list.html')
        self.assertContains(response, 'Kod produktu')
        self.assertContains(response, 'Stan ')
        self.assertContains(response, 'Szukaj')
        self.assertContains(response, 'Lista maszyn')
        self.assertNotContains(response, 'Admin panel')

    def test_update_product_info_works(self):
        response = self.client.get(reverse('supply_info:update_product_info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/update_product_info.html')
        self.assertContains(response, 'Import produktów')

    def test_update_product_availability_works(self):
        response = self.client.get(reverse('supply_info:update_product_availability'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/update_product_info.html')
        self.assertContains(response, 'Uaktualnij stany')


class TestPageAnonymous(TestCase):

    def test_machines_list_page_works(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/machines_list.html')
        self.assertContains(response, 'Kod produktu')
        self.assertNotContains(response, 'Stan ')
        self.assertNotContains(response, 'Szukaj')
        self.assertNotContains(response, 'Lista maszyn')
        self.assertNotContains(response, 'Admin panel')

    def test_update_product_info_works(self):
        response = self.client.get(reverse('supply_info:update_product_info'))
        self.assertEqual(response.status_code, 302)

    def test_update_product_availability_works(self):
        response = self.client.get(reverse('supply_info:update_product_availability'))
        self.assertEqual(response.status_code, 302)
