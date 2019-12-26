import datetime

from django.test import TestCase
from django.views import generic
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, force_authenticate
from supply_info import views
from supply_info.models import Product, ProductAvailability


class AdminInTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1', name='machine_1 desc', type='maszyny'
        )
        a = ProductAvailability(product_code=Product.objects.get(code="Machine1"), availability=10)
        a.save()
        Product.objects.create(
            code='Machine2', name='machine_2 desc'
        )
        b = ProductAvailability(product_code=Product.objects.get(code="Machine2"), availability=20)
        b.save()
        self.user = User.objects.create_superuser('Artur_admin', 'artur_the_admin@example.com', 'arturadminpassword')


class UserInTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1', name='machine_1 desc'
        )
        a = ProductAvailability(product_code=Product.objects.get(code="Machine1"), availability=10)
        a.save()
        Product.objects.create(
            code='Machine2', name='machine_2 desc'
        )
        b = ProductAvailability(product_code=Product.objects.get(code="Machine2"), availability=20)
        b.save()
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')


class TestApiProductListAsAdmin(AdminInTestCase):

    def test_get(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().get('api/products/')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().post('api/products/',  {"code": "prod1", "name":"desc1"}, format='json')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 201)


class TestApiProductListAsUser(UserInTestCase):

    def test_get(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().get('api/products/')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().post('api/products/',  {"code": "prod1", "name":"desc1"}, format='json')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 401)


class TestApiProductListAsUnauthorized(TestCase):

    def test_get(self):
        req = APIRequestFactory().get('api/products/')
        resp = views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 401)

    def test_post(self):
        req = APIRequestFactory().post('api/products/',  {"code": "prod1", "name":"desc1"}, format='json')
        resp = views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 401)


class TestApiProductDetailAsAdmin(AdminInTestCase):

    def test_get(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().get('api/products/Machine1')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 200)

    def test_put(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().put('api/products/Machine1',  {'code': 'Machine1', 'site_address':'www.m1.com'})
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().delete('api/products/Machine1')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 204)


class TestApiProductDetailAsUser(UserInTestCase):

    def test_get(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().get('api/products/Machine1')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 200)

    def test_put(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().put('api/products/Machine1',  {'code': 'Machine1', 'site_address':'www.m1.com'})
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)

    def test_delete(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().delete('api/products/Machine1')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)


class TestApiProductDetailAsUnauthorized(TestCase):
    def test_get(self):
        req = APIRequestFactory().get('api/products/Machine1')
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)

    def test_put(self):
        req = APIRequestFactory().put('api/products/Machine1',  {'code': 'Machine1', 'site_address':'www.m1.com'})
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)

    def test_delete(self):
        req = APIRequestFactory().delete('api/products/Machine1')
        resp = views.ApiProductDetail.as_view()(req, code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)


class TestApiAvailabilityListAsAdmin(AdminInTestCase):
    def test_get(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().get('api/availability/')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiAvailabilityList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)


class TestApiAvailabilityListAsUser(UserInTestCase):
    def test_get(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().get('api/availability/')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiAvailabilityList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)


class TestApiAvailabilityListAsUnauthorized(TestCase):
    def test_get(self):
        req = APIRequestFactory().get('api/availability/')
        resp = views.ApiAvailabilityList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 401)


class TestApiAvailabilityDetailAsAdmin(AdminInTestCase):
    def test_get(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().get('api/availability/Machine1')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
        self.assertEqual(resp.status_code, 200)

    def test_put(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().put('api/availability/Machine1',  {'product_code': 'Machine1', 'availability':5})
        force_authenticate(req, user=user, token=None)
        resp = views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
        self.assertEqual(resp.status_code, 200)


class TestApiAvailabilityDetailAsUser(UserInTestCase):
    def test_get(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().get('api/availability/Machine1')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
        self.assertEqual(resp.status_code, 200)

    def test_put(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().put('api/availability/Machine1',  {'product_code': 'Machine1', 'availability':5})
        force_authenticate(req, user=user, token=None)
        resp = views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)


class TestApiAvailabilityDetailAsUnauthorized(TestCase):
    def test_get(self):
        req = APIRequestFactory().get('api/availability/Machine1')
        resp = views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)

    def test_put(self):
        req = APIRequestFactory().put('api/availability/Machine1',  {'product_code': 'Machine1', 'availability':5})
        resp = views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
        self.assertEqual(resp.status_code, 401)


class TestApiMachinesAvailabilityListAsAdmin(AdminInTestCase):
    def test_get(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().get('api/machines/')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiMachinesAvailabilityList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)


class TestApiMachinesAvailabilityListAsUser(UserInTestCase):
    def test_get(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().get('api/machines/')
        force_authenticate(req, user=user, token=None)
        resp = views.ApiMachinesAvailabilityList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)


class TestApiMachinesAvailabilityListAsUnauthorized(TestCase):
    def test_get(self):
        req = APIRequestFactory().get('api/machines/')
        resp = views.ApiMachinesAvailabilityList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 401)