from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from supply_info import api_views
from supply_info.models import Product
from supply_info.serializers import ProductSerializer, ProductCodeSerializer


class AdminInTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            type='maszyny',
            availability=10,
            is_active=True,
        )
        Product.objects.create(
            code='Machine2',
            name='machine_2 desc',
            availability=20,
            is_active=True,
        )
        self.user = User.objects.create_superuser('Artur_admin', 'artur_the_admin@example.com', 'arturadminpassword')


class UserInTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            code='Machine1',
            name='machine_1 desc',
            availability=10

        )
        Product.objects.create(
            code='Machine2',
            name='machine_2 desc',
            availability=20
        )
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')


class TestApiProductListAsAdmin(AdminInTestCase):

    active_products_list = Product.objects.filter(is_active=True)

    def test_products_get(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().get('api/products/')
        force_authenticate(req, user=user, token=None)
        resp = api_views.ApiProductList.as_view()(req, *[], **{})
        serializer_data = ProductSerializer(self.active_products_list, many=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, serializer_data.data)

    def test_product_post(self):
        user = User.objects.get(username='Artur_admin')
        req = APIRequestFactory().post('api/products/',  [{"code": "prod1", "name": "desc1"}], format='json')
        force_authenticate(req, user=user, token=None)
        resp = api_views.ApiProductList.as_view()(req, *[], **{})
        expected_resp = [{
            'code': 'prod1',
            'manufacturer': None,
            'name': 'desc1',
            'prod_group': None,
            'type': 'Akcesoria',
            'sub_type': 'Inne',
            'mark': None,
            'site_address': None,
            'availability': 0,
            'is_active': False,
            'price_a': None,
            'price_b': None,
            'price_c': None,
            'price_d': None
        }]

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(expected_resp, resp.data)

    def test_product_put(self):
        user = User.objects.get(username='Artur_admin')
        req_data = [
            {
                'code': 'Machine1',
                'availability': 9,
                'is_active': True,
                'price_a': 10,
                'price_b': 8,
                'price_c': 8,
                'price_d': 12
            },
            {
                'code': 'Machine2',
                'availability': 20,
                'is_active': False,
                'price_a': 10.00,
                'price_b': 8.00,
                'price_c': 8.00,
                'price_d': 12.00
            }
        ]
        req = APIRequestFactory().put('api/products/',  req_data, format='json')
        force_authenticate(req, user=user, token=None)
        resp = api_views.ApiProductList.as_view()(req, *[], **{})
        new_active_products_list = Product.objects.filter(is_active=True)
        serializer_data = ProductSerializer(new_active_products_list, many=True)
        new_req = APIRequestFactory().get('api/products/')
        force_authenticate(new_req, user=user, token=None)
        new_resp = api_views.ApiProductList.as_view()(new_req, *[], **{})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(new_resp.data), 1)
        self.assertEqual(req_data[0].get('availability'), new_resp.data[0].get('availability'))
        self.assertEqual(req_data[0].get('price_a'), float(new_resp.data[0].get('price_a')))
        self.assertEqual(req_data[0].get('price_b'), float(new_resp.data[0].get('price_b')))
        self.assertEqual(req_data[0].get('price_c'), float(new_resp.data[0].get('price_c')))
        self.assertEqual(req_data[0].get('price_d'), float(new_resp.data[0].get('price_d')))


class TestApiProductListAsUser(UserInTestCase):

    def test_get(self):
        user = User.objects.get(username='adam')
        req = APIRequestFactory().get('api/products/')
        force_authenticate(req, user=user, token=None)
        resp = api_views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)

    # def test_post(self):
    #     user = User.objects.get(username='adam')
    #     req = APIRequestFactory().post('api/products/',  {"code": "prod1", "name":"desc1"}, format='json')
    #     force_authenticate(req, user=user, token=None)
    #     resp = api_views.ApiProductList.as_view()(req, *[], **{})
    #     self.assertEqual(resp.status_code, 403)


class TestApiProductListAsUnauthorized(TestCase):

    def test_get(self):
        req = APIRequestFactory().get('api/products/')
        resp = api_views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 401)

    def test_post(self):
        req = APIRequestFactory().post('api/products/',  {"code": "prod1", "name":"desc1"}, format='json')
        resp = api_views.ApiProductList.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 401)


# class TestApiProductDetailAsAdmin(AdminInTestCase):
#
#     def test_get(self):
#         user = User.objects.get(username='Artur_admin')
#         req = APIRequestFactory().get('api/products/Machine1')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 200)
#
#     def test_put(self):
#         user = User.objects.get(username='Artur_admin')
#         req = APIRequestFactory().put('api/products/Machine1',  {'code': 'Machine1', 'site_address':'www.m1.com'})
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 200)
#
#     def test_delete(self):
#         user = User.objects.get(username='Artur_admin')
#         req = APIRequestFactory().delete('api/products/Machine1')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 204)


# class TestApiProductDetailAsUser(UserInTestCase):
#
#     def test_get(self):
#         user = User.objects.get(username='adam')
#         req = APIRequestFactory().get('api/products/Machine1')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 200)
#
#     def test_put(self):
#         user = User.objects.get(username='adam')
#         req = APIRequestFactory().put('api/products/Machine1',  {'code': 'Machine1', 'site_address':'www.m1.com'})
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)
#
#     def test_delete(self):
#         user = User.objects.get(username='adam')
#         req = APIRequestFactory().delete('api/products/Machine1')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)


# class TestApiProductDetailAsUnauthorized(TestCase):
#     def test_get(self):
#         req = APIRequestFactory().get('api/products/Machine1')
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)
#
#     def test_put(self):
#         req = APIRequestFactory().put('api/products/Machine1',  {'code': 'Machine1', 'site_address':'www.m1.com'})
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)
#
#     def test_delete(self):
#         req = APIRequestFactory().delete('api/products/Machine1')
#         resp = api_views.ApiProductDetail.as_view()(req, code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)


# class TestApiAvailabilityListAsAdmin(AdminInTestCase):
#     def test_get(self):
#         user = User.objects.get(username='Artur_admin')
#         req = APIRequestFactory().get('api/availability/')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiAvailabilityList.as_view()(req, *[], **{})
#         self.assertEqual(resp.status_code, 200)
#
#
# class TestApiAvailabilityListAsUser(UserInTestCase):
#     def test_get(self):
#         user = User.objects.get(username='adam')
#         req = APIRequestFactory().get('api/availability/')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiAvailabilityList.as_view()(req, *[], **{})
#         self.assertEqual(resp.status_code, 200)
#
#
# class TestApiAvailabilityListAsUnauthorized(TestCase):
#     def test_get(self):
#         req = APIRequestFactory().get('api/availability/')
#         resp = api_views.ApiAvailabilityList.as_view()(req, *[], **{})
#         self.assertEqual(resp.status_code, 401)
#
#
# class TestApiAvailabilityDetailAsAdmin(AdminInTestCase):
#     def test_get(self):
#         user = User.objects.get(username='Artur_admin')
#         req = APIRequestFactory().get('api/availability/Machine1')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
#         self.assertEqual(resp.status_code, 200)
#
#     def test_put(self):
#         user = User.objects.get(username='Artur_admin')
#         req = APIRequestFactory().put('api/availability/Machine1',  {'product_code': 'Machine1', 'availability':5})
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
#         self.assertEqual(resp.status_code, 200)
#
#
# class TestApiAvailabilityDetailAsUser(UserInTestCase):
#     def test_get(self):
#         user = User.objects.get(username='adam')
#         req = APIRequestFactory().get('api/availability/Machine1')
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
#         self.assertEqual(resp.status_code, 200)
#
#     def test_put(self):
#         user = User.objects.get(username='adam')
#         req = APIRequestFactory().put('api/availability/Machine1',  {'product_code': 'Machine1', 'availability':5})
#         force_authenticate(req, user=user, token=None)
#         resp = api_views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)


# class TestApiAvailabilityDetailAsUnauthorized(TestCase):
#     def test_get(self):
#         req = APIRequestFactory().get('api/availability/Machine1')
#         resp = api_views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)
#
#     def test_put(self):
#         req = APIRequestFactory().put('api/availability/Machine1',  {'product_code': 'Machine1', 'availability':5})
#         resp = api_views.ApiAvailabilityDetail.as_view()(req, product_code='Machine1', **{})
#         self.assertEqual(resp.status_code, 401)


