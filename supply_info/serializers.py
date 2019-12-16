from rest_framework import serializers
from .models import Product, ProductAvailability, ActiveProductList
from django.contrib.auth.models import User


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=200)
    prod_group = serializers.CharField(required=False, allow_blank=True, max_length=60)

    def create(self, validated_data):
        return ProductSerializer.object.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.prod_group = validated_data.get('prod_group')