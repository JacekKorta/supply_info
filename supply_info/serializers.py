from rest_framework import serializers
from .models import Product, ProductAvailability, ActiveProductList
from django.contrib.auth.models import User


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(required=False, allow_blank=True, max_length=30)
    sub_type = serializers.CharField(required=False, allow_blank=True, max_length=30)

    def create(self, validated_data):
        return ProductSerializer.object.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.sub_type = validated_data.get('sub_type', instance.sub_type)
