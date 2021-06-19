from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from supply_info.models import Product


class LoggedInTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            type='maszyny',
            mark='M',
            price_a=10,
            price_b=5,
            price_c=7,
            price_d=15,
            is_active=True,
            availability=10
        )

        group_name = "Dystrybutorzy_B"
        self.group_b = Group(name=group_name)
        self.group_b.save()
        group_name = "Dystrybutorzy_C"
        self.group_c = Group(name=group_name)
        self.group_c.save()

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
        self.assertContains(response, 'administracja')
        self.assertContains(response, 'magazyn')



class TestPageLogged(LoggedInTestCase):
    def test_machines_list_page_works(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/machines_list.html')
        self.assertContains(response, 'Kod produktu')
        self.assertContains(response, 'Stan ')
        self.assertContains(response, 'Szukaj')
        self.assertContains(response, 'Lista maszyn')
        self.assertNotContains(response, 'administracja')
        self.assertNotContains(response, 'Magazyn')


class TestPageAnonymous(TestCase):
    def test_machines_list_page_works(self):
        response = self.client.get(reverse('supply_info:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supply_info/machines_list.html')
        self.assertContains(response, 'Kod produktu')
        self.assertNotContains(response, 'Stan ')
        self.assertNotContains(response, 'Szukaj')
        self.assertNotContains(response, 'Lista maszyn')
        self.assertNotContains(response, 'Administracja')
        self.assertNotContains(response, 'Magazyn')

