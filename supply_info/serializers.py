from rest_framework import serializers

from supply_info.models import Product


class ProductSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProductSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.sub_type = validated_data.get('sub_type', instance.sub_type)
        instance.next_shipment = validated_data.get('next_shipment', instance.next_shipment)
        instance.site_address = validated_data.get('site_address', instance.site_address)
        instance.price_a = validated_data.get('price_a', instance.price_a)
        instance.price_b = validated_data.get('price_b', instance.price_b)
        instance.price_c = validated_data.get('price_c', instance.price_c)
        instance.price_d = validated_data.get('price_d', instance.price_d)
        instance.availability = validated_data.get('availability', instance.price_d)
        instance.is_active = validated_data.get('is_active', instance.price_d)
        instance.save()
        return instance

    class Meta:
        fields = (
            "code",
            "manufacturer",
            "name",
            "prod_group",
            "type",
            "sub_type",
            "mark",
            "site_address",
            "availability",
            "is_active",
            "price_a",
            "price_b",
            "price_c",
            "price_d",
        )
        model = Product


class ProductCodeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("code",)
        model = Product
