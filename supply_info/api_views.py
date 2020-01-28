from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .sp_modules import db_save
from .serializers import ProductSerializer, ProductAvailabilitySerializer
from .models import Product, ProductAvailability


class ApiProductList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.is_superuser:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ApiProductDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, code):
        try:
            code = code.replace('%20', ' ')
            return Product.objects.get(code=code)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        product = self.get_object(code)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, code, format=None):
        if request.user.is_superuser:
            product = self.get_object(code)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, code, format=None):
        if request.user.is_superuser:
            product = self.get_object(code)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ApiAvailabilityList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        availability = ProductAvailability.objects.all()
        serializer = ProductAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)


class ApiAvailabilityDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, product_code):
        try:
            product_code = product_code.replace('%20', ' ')
            return ProductAvailability.objects.get(product_code=Product.objects.get(code=product_code))
        except ProductAvailability.DoesNotExist:
            raise Http404

    def get(self, request, product_code, format=None):
        availability_ob = self.get_object(product_code)
        serializer = ProductAvailabilitySerializer(availability_ob)
        return Response(serializer.data)

    def put(self, request, product_code, format=None):
        if request.user.is_superuser:
            availability_ob = self.get_object(product_code)
            serializer = ProductAvailabilitySerializer(availability_ob, data=request.data)
            if serializer.is_valid():
                serializer.save()
                db_save.event_record(request.user.username, 'availability update')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)