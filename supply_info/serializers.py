

from rest_framework import serializers
from .models import Product, ProductAvailability, ActiveProductList
from django.contrib.auth.models import User


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(required=False, allow_blank=True, max_length=30)
    sub_type = serializers.CharField(required=False, allow_blank=True, max_length=30)
    next_shipment = serializers.CharField(required=False, allow_blank=True, max_length=12)
    site_address = serializers.CharField(required=False, allow_blank=True, max_length=120)

    def create(self, validated_data):
        return ProductSerializer.object.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.sub_type = validated_data.get('sub_type', instance.sub_type)
        instance.next_shipment = validated_data.get('next_shipment', instance.next_shipment)
        instance.site_address = validated_data.get('site_address', instance.site_address)


class ProductAvailabilitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_code = serializers.CharField(max_length=100)
    availability = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.availability = validated_data.get('availability', instance.availability)

