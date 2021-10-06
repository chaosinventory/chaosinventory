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


class NestedItemSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='item-detail')

    class Meta:
        model = Item
        fields = [
            '_url',
            'id',
            'name',
            'note',
            'amount',
            'belongs_to_id',
            'actual_location_id',
            'target_location_id',
            'product_id',
            'target_item_id',
            'actual_item_id',
        ]


class ItemSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='item-detail')

    belongs_to = EntitySerializer(
        read_only=True,
    )
    belongs_to_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='belongs_to',
        queryset=Entity.objects.all(),
    )

    actual_location = LocationSerializer(
        read_only=True,
    )
    actual_location_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='actual_location',
        queryset=Location.objects.all(),
    )

    target_location = LocationSerializer(
        read_only=True,
    )
    target_location_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='target_location',
        queryset=Location.objects.all(),
    )

    product = ProductSerializer(
        read_only=True,
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
    )

    target_item = NestedItemSerializer(
        read_only=True,
    )
    target_item_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='target_item',
        queryset=Item.objects.all(),
    )

    actual_item = NestedItemSerializer(
        read_only=True,
    )
    actual_item_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='actual_item',
        queryset=Item.objects.all(),
    )

    iteminventoryid_set = ItemInventoryIdSerializer(
        read_only=True,
        many=True,
    )
    iteminventoryid_id_set = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='iteminventoryid_set',
        queryset=ItemInventoryId.objects.all(),
    )

    itemdata_set = ItemDataSerializer(
        read_only=True,
        many=True,
    )
    itemdata_id_set = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='itemdata_set',
        queryset=ItemData.objects.all(),
    )

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='tags',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Item
        fields = [
            '_url',
            'id',
            'name',
            'note',
            'amount',
            'belongs_to',
            'belongs_to_id',
            'actual_location',
            'actual_location_id',
            'target_location',
            'target_location_id',
            'product',
            'product_id',
            'target_item',
            'target_item_id',
            'actual_item',
            'actual_item_id',
            'iteminventoryid_set',
            'iteminventoryid_id_set',
            'itemdata_set',
            'itemdata_id_set',
            'tags',
            'tag_ids',
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
