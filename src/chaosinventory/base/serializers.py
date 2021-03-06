from rest_framework import serializers

from .models import (
    DataType, Entity, Item, ItemInventoryId, Location, LocationData, Product,
    ProductData, ProductInventoryId, Tag,
)


class CommonBasicInventoryIdSerializer(serializers.ModelSerializer):
    # Only using a PK-Related field since this would be another level
    # of recursion with a high degree of redundancy and little use.
    schema = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = ProductInventoryId
        fields = [
            'id',
            'value',
            'schema',
        ]


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
            'name',
            'parent'
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


class BasicLocationDataSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type'
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
            'id',
            'name',
            'note',
            'part_of',  # TODO: Make recursive?
            'tags',
        ]


class BasicProductInventoryIdSerializer(CommonBasicInventoryIdSerializer):
    class Meta(CommonBasicInventoryIdSerializer.Meta):
        model = ProductInventoryId


class BasicItemInventoryIdSerializer(CommonBasicInventoryIdSerializer):
    class Meta(CommonBasicInventoryIdSerializer.Meta):
        model = ItemInventoryId


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    productdata_set = BasicProductDataSerializer(
        many=True,
        required=False
    )

    productinventoryid_set = BasicProductInventoryIdSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'note',
            'tags',
            'productinventoryid_set',
            'productdata_set',
        ]


class ItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    belongs_to = EntitySerializer
    product = ProductSerializer
    target_location = LocationSerializer
    actual_location = LocationSerializer

    iteminventoryid_set = BasicItemInventoryIdSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'note',
            'amount',
            'belongs_to',
            'actual_location',
            'target_location',
            'product',
            'target_item',  # TODO: Make recursive?
            'actual_item',  # TODO: Make recursive?
            'iteminventoryid_set',
            'tags',
        ]
