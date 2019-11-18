from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')


class TestPageLogged(LoggedInTestCase):
    def test_machine_list_page_works(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/machine_list.html')
        self.assertContains(response, 'Kod produktu')

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
    def test_machine_list_page_works(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/machine_list.html')
        self.assertContains(response, 'Kod produktu')

    def test_update_product_info_works(self):
        response = self.client.get(reverse('supply_info:update_product_info'))
        self.assertEqual(response.status_code, 302)

    def test_update_product_availability_works(self):
        response = self.client.get(reverse('supply_info:update_product_availability'))
        self.assertEqual(response.status_code, 302)
