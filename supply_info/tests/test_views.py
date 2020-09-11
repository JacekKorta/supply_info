from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from supply_info.models import Product, PriceList, ProductAvailability, ActiveProductList


class LoggedInTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            type='maszyny',
            mark='M'
        )
        ProductAvailability.objects.create(product_code=Product.objects.get(code="Machine1"), availability=10)
        a = ActiveProductList(product_code=Product.objects.get(code="Machine1"))
        a.is_active = True
        a.save()
        p = PriceList(product_code=Product.objects.get(code='Machine1'),
                      price_a=10,
                      price_b=5,
                      price_c=7,
                      price_d=15,)
        p.save()

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

    def test_update_product_info_works(self):
        response = self.client.get(reverse('supply_info:update_product_info'))
        self.assertEqual(response.status_code, 302)

    def test_update_product_availability_works(self):
        response = self.client.get(reverse('supply_info:update_product_availability'))
        self.assertEqual(response.status_code, 302)

    """
    def test_search_view_user_group_b(self):
        self.user.groups.add(self.group_b)
        self.user.save()
        results = Product.objects.prefetch_related('price_lists',
                                                   'product_availability').filter(code='Machine1').order_by('code')
        response = self.client.get(reverse('supply_info:search_product'))
    """


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

    def test_update_product_info_works(self):
        response = self.client.get(reverse('supply_info:update_product_info'))
        self.assertEqual(response.status_code, 302)

    def test_update_product_availability_works(self):
        response = self.client.get(reverse('supply_info:update_product_availability'))
        self.assertEqual(response.status_code, 302)
