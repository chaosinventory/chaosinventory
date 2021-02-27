from rest_framework import serializers

from .models import (
    DataType, Entity, Item, Location, LocationData, Product, ProductData, Tag,
)


class BasicLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'note',
            'in_location'  # TODO: Make recursive?
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'parent'
        ]


class BasicLocationDataSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type'
        ]


class BasicProductDataSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = ProductData
        fields = [
            'id',
            'value',
            'type'
        ]


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = [
            'id',
            'name',
            'note'
        ]


class LocationDataSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(source='type.name')
    location = BasicLocationSerializer()

    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type',
            'location'
        ]


class LocationSerializer(serializers.ModelSerializer):
    locationdata_set = BasicLocationDataSerializer(many=True, required=False)

    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'note',
            'in_location',
            'locationdata_set'
        ]


class EntitySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Entity
        fields = [
            'name',
            'note',
            'part_of',  # TODO: Make recursive?
            'tags',
        ]


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    productdata_set = BasicLocationDataSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'note',
            'tags',
            'inventory_id',
            'productdata_set',
        ]


class ItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    belongs_to = EntitySerializer
    product = ProductSerializer
    target_location = LocationSerializer
    actual_location = LocationSerializer

    class Meta:
        model = Item
        fields = [
            'name',
            'note',
            'amount',
            'belongs_to',
            'actual_location',
            'target_location',
            'product',
            'target_item',  # TODO: Make recursive?
            'actual_item',  # TODO: Make recursive?
            'inventory_id',  # TODO: Rework once #24 is merged
            'tags',
        ]
