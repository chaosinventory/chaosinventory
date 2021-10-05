from rest_framework import serializers

from .models import (
    DataType, Entity, InventoryIdSchema, Item, ItemData, ItemInventoryId,
    Location, LocationData, Overlay, OverlayItem, Product, ProductData,
    ProductInventoryId, Tag,
)


class ProductInventoryIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryId
        fields = [
            'id',
            'value',
            'schema',
        ]


class InventoryIdSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryIdSchema
        fields = [
            'id',
            'name',
            'note',
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'note',
            'in_location',
            'locationdata_set',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'parent'
        ]


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = [
            'id',
            'name',
            'note',
        ]


class ItemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemData
        fields = [
            'id',
            'value',
            'type',
            'item',
        ]


class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductData
        fields = [
            'id',
            'value',
            'type',
            'product'
        ]


class LocationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type',
            'location',
        ]


class LocationSerializer(serializers.ModelSerializer):
    locationdata_set = LocationDataSerializer(many=True, required=False, read_only=True)
    in_location = LocationSerializer()

    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'note',
            'in_location',
            'locationdata_set'
        ]


class LocationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type',
            'location'
        ]


class OverlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Overlay
        fields = [
            'id',
            'name',
            'note',
            'active',
            'parent',
            'overlayitem_set',
        ]


class OverlayItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverlayItem
        fields = [
            'id',
            'overlay',
            'item',
            'target_item',
            'target_location',
        ]


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = [
            'id',
            'name',
            'note',
            'part_of',
            'tags',
        ]


class ProductInventoryIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryId
        fields = [
            'id',
            'value',
            'schema',
            'product',
        ]


class ItemInventoryIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInventoryId
        fields = [
            'id',
            'value',
            'schema',
            'item',
        ]

class ProductSerializer(serializers.ModelSerializer):
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
            'target_item',
            'actual_item',
            'iteminventoryid_set',
            'itemdata_set',
            'tags',
        ]


class ItemDataSerializer(serializers.ModelSerializer):
    type = DataTypeSerializer()
    item = ItemSerializer()

    class Meta:
        model = ItemData
        fields = [
            'id',
            'value',
            'type',
            'item',
        ]
