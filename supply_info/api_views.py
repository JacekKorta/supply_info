import logging

from rest_framework import status, generics
from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import ValidationError

from supply_info.models import Product
from supply_info.serializers import ProductSerializer, ProductCodeSerializer
from supply_info.sp_modules import db_save


logger = logging.getLogger(__name__)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS) and request.user.is_active:
            return True
        return request.user.is_superuser


class ApiProductUpdateView(generics.UpdateAPIView):
    lookup_field = 'code'
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ApiProductList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (AllowAny,)

    def get_object(self, obj_code):
        try:
            return Product.objects.get(code=obj_code)
        except (Product.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, format=None):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            db_save.event_record(request.user.username, 'availability update')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None, *args, **kwargs):
        errors = []
        try:
            for item in request.data:
                code = item.get('code')
                price_a = item.get('price_a', 0)
                price_b = item.get('price_b', 0)
                price_c = item.get('price_c', 0)
                price_d = item.get('price_d', 0)
                availability = item.get('availability', 0)
                mark = item.get("mark", '')
                try:
                    product = Product.objects.get(code=code)
                    if product.synchronize:
                        product.price_a = price_a
                        product.price_b = price_b
                        product.price_c = price_c
                        product.price_d = price_d
                        product.availability = availability
                        product.mark = mark
                        product.save()
                except Product.DoesNotExist:
                    logger.warning(f"Product: {code} - does not exist")
                    errors.append(f"Product: {code} - does not exist")
                except Exception as e:
                    logger.error(f"error {e}, during procesing product: {code}")
                    errors.append(f"error {e}, during procesing product: {code}")
        except Exception as e:
            logger.error(e)
            errors.append(e)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        db_save.event_record(request.user.username, 'availability update')
        return Response(errors, status=status.HTTP_200_OK)


class ApiProductCodeList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        products = Product.objects
        serializer = ProductCodeSerializer(products, many=True)
        return Response(serializer.data)