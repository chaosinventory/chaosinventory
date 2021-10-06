from rest_framework import serializers

from .models import (
    DataType, Entity, InventoryIdSchema, Item, ItemData, ItemInventoryId,
    Location, LocationData, Overlay, OverlayItem, Product, ProductData,
    ProductInventoryId, Tag,
)


class NestedTagSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='tag-detail')

    class Meta:
        model = Tag
        fields = [
            '_url',
            'id',
            'name',
            'parent_id',
        ]


class TagSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='tag-detail')

    parent = NestedTagSerializer(
        read_only=True,
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='parent',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Tag
        fields = [
            '_url',
            'id',
            'name',
            'parent',
            'parent_id',
        ]


class DataTypeSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='datatype-detail')

    class Meta:
        model = DataType
        fields = [
            '_url',
            'id',
            'name',
            'note',
        ]


class NestedEntitySerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='entity-detail')

    class Meta:
        model = Entity
        fields = [
            '_url',
            'id',
            'name',
            'note',
            'part_of_id',
        ]


class EntitySerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='entity-detail')

    part_of = NestedEntitySerializer(
        read_only=True,
    )
    part_of_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='part_of',
        queryset=Entity.objects.all(),
    )

    tags = NestedTagSerializer(
        required=False,
        allow_null=True,
        many=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='tags',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Entity
        fields = [
            '_url',
            'id',
            'name',
            'note',
            'part_of',
            'part_of_id',
            'tags',
            'tag_ids',
        ]


class NestedLocationDataSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='locationdata-detail')

    type = DataTypeSerializer(
        read_only=True,
    )
    type_id = serializers.PrimaryKeyRelatedField(
        source='type',
        queryset=DataType.objects.all(),
    )

    class Meta:
        model = LocationData
        fields = [
            '_url',
            'id',
            'value',
            'type',
            'type_id',
            'location_id',
        ]


class NestedProductDataSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='productinventoryid-detail')

    type = DataTypeSerializer(
        read_only=True,
    )
    type_id = serializers.PrimaryKeyRelatedField(
        source='type',
        queryset=DataType.objects.all(),
    )


    class Meta:
        model = ProductData
        fields = [
            '_url',
            'id',
            'value',
            'type',
            'type_id',
            'product_id',
        ]


class InventoryIdSchemaSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='inventoryidschema-detail')

    class Meta:
        model = InventoryIdSchema
        fields = [
            '_url',
            'id',
            'name',
            'note',
        ]


class NestedProductInventoryIdSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='productinventoryid-detail')

    schema = InventoryIdSchemaSerializer(
        read_only=True,
    )
    schema_id = serializers.PrimaryKeyRelatedField(
        source='schema',
        queryset=InventoryIdSchema.objects.all(),
    )

    class Meta:
        model = ProductInventoryId
        fields = [
            '_url',
            'id',
            'value',
            'schema',
            'schema_id',
            'product_id',
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


class NestedLocationSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='location-detail')

    class Meta:
        model = Location
        fields = [
            '_url',
            'id',
            'name',
            'note',
            'in_location_id',
        ]


class LocationSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='location-detail')


    in_location = NestedLocationSerializer(
        read_only=True,
    )
    in_location_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='in_location',
        queryset=Location.objects.all(),
    )

    locationdata_set = NestedLocationDataSerializer(
        read_only=True,
        many=True,
    )
    locationdata_id_set = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='locationdata_set',
        queryset=LocationData.objects.all(),
    )


    class Meta:
        model = Location
        fields = [
            '_url',
            'id',
            'name',
            'note',
            'in_location',
            'in_location_id',
            'locationdata_set',
            'locationdata_id_set',
        ]


class LocationDataSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='locationdata-detail')

    type = DataTypeSerializer(
        read_only=True,
    )
    type_id = serializers.PrimaryKeyRelatedField(
        source='type',
        queryset=DataType.objects.all(),
    )

    location = NestedLocationSerializer(
        read_only=True,
    )
    location_id = serializers.PrimaryKeyRelatedField(
        source='location',
        queryset=Location.objects.all(),
    )


    class Meta:
        model = LocationData
        fields = [
            '_url',
            'id',
            'value',
            'type',
            'type_id',
            'location',
            'location_id',
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


class ItemInventoryIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInventoryId
        fields = [
            'id',
            'value',
            'schema',
            'item',
        ]


class NestedProductSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='product-detail')

    class Meta:
        model = Product
        fields = [
            '_url',
            'id',
            'name',
            'note',
        ]


class ProductSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='product-detail')

    productinventoryid_set = NestedProductInventoryIdSerializer(
        read_only=True,
        many=True,
    )
    productinventoryid_id_set = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='productinventoryid_set',
        queryset=ProductInventoryId.objects.all(),
    )

    productdata_set = NestedProductDataSerializer(
        read_only=True,
        many=True,
    )
    productdata_id_set = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='productdata_set',
        queryset=ProductData.objects.all(),
    )

    tags = NestedTagSerializer(
        required=False,
        allow_null=True,
        many=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        source='tags',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Product
        fields = [
            '_url',
            'id',
            'name',
            'note',
            'productinventoryid_set',
            'productinventoryid_id_set',
            'productdata_set',
            'productdata_id_set',
            'tags',
            'tag_ids',
        ]


class ProductInventoryIdSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='productinventoryid-detail')

    schema = InventoryIdSchemaSerializer(
        read_only=True,
    )
    schema_id = serializers.PrimaryKeyRelatedField(
        source='schema',
        queryset=InventoryIdSchema.objects.all(),
    )

    product = NestedProductSerializer(
        read_only=True,
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
    )

    class Meta:
        model = ProductInventoryId
        fields = [
            '_url',
            'id',
            'value',
            'schema',
            'schema_id',
            'product',
            'product_id',
        ]


class ProductDataSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(view_name='productinventoryid-detail')

    type = DataTypeSerializer(
        read_only=True,
    )
    type_id = serializers.PrimaryKeyRelatedField(
        source='type',
        queryset=DataType.objects.all(),
    )

    product = NestedProductSerializer(
        read_only=True,
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
    )

    class Meta:
        model = ProductData
        fields = [
            '_url',
            'id',
            'value',
            'type',
            'type_id',
            'product',
            'product_id',
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

    belongs_to = NestedEntitySerializer(
        read_only=True,
    )
    belongs_to_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='belongs_to',
        queryset=Entity.objects.all(),
    )

    actual_location = NestedLocationSerializer(
        read_only=True,
    )
    actual_location_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='actual_location',
        queryset=Location.objects.all(),
    )

    target_location = NestedLocationSerializer(
        read_only=True,
    )
    target_location_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='target_location',
        queryset=Location.objects.all(),
    )

    product = NestedProductSerializer(
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

    tags = NestedTagSerializer(
        required=False,
        allow_null=True,
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
