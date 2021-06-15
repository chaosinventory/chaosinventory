from rest_framework import serializers

from .models import (
    DataType, Entity, InventoryIdSchema, Item, ItemData, ItemInventoryId,
    Location, LocationData, Overlay, OverlayItem, Product, ProductData,
    ProductInventoryId, Tag,
)


class CommonBasicInventoryIdSerializer(serializers.ModelSerializer):
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


class BasicLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'note',
            'in_location',
            'locationdata_set',
        ]


class BasicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'parent'
        ]

    def validate(self, data):
        """
        When the object is updated, self.instance still is the original
        instance. If we validate on that, we could use self as a parent
        but not change it afterwards. Thus, as far as I know, we cant
        use validators on the models.
        """

        if ('parent' in data and
            data['parent'] is not None and
            self.instance is not None and
                data['parent'].pk == self.instance.pk):

            raise serializers.ValidationError(
                {'parent': "Must not be self"},
            )

        return data


class TagSerializer(BasicTagSerializer):
    parent = BasicTagSerializer(required=False)

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'parent',
        ]


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = [
            'id',
            'name',
            'note',
        ]


class BasicItemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemData
        fields = [
            'id',
            'value',
            'type',
            'item',
        ]


class BasicProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductData
        fields = [
            'id',
            'value',
            'type',
            'product'
        ]


class WritableLocationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type',
            'location',
        ]


class BasicLocationDataSerializer(WritableLocationDataSerializer):
    type = DataTypeSerializer()


class LocationSerializer(serializers.ModelSerializer):
    locationdata_set = BasicLocationDataSerializer(many=True, required=False, read_only=True)
    in_location = BasicLocationSerializer()

    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'note',
            'in_location',
            'locationdata_set'
        ]

    def validate(self, data):
        """
        See TagSerializer.validate().
        """

        if (data['in_location'] is not None and
            self.instance is not None and
                data['in_location'].pk == self.instance.pk):

            raise serializers.ValidationError(
                {'in_location': "Must not be self"},
            )

        return data


class LocationDataSerializer(serializers.ModelSerializer):
    type = DataTypeSerializer()
    location = BasicLocationSerializer()

    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type',
            'location'
        ]


class BasicOverlaySerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        """
        See TagSerializer.validate().
        """

        if (data['parent'] is not None and
            self.instance is not None and
                data['parent'].pk == self.instance.pk):

            raise serializers.ValidationError(
                {'parent': "Must not be self"},
            )

        return data


class WritableOverlayItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverlayItem
        fields = [
            'id',
            'overlay',
            'item',
            'target_item',
            'target_location',
        ]


class BasicEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = [
            'id',
            'name',
            'note',
            'part_of',
            'tags',
        ]

    def validate(self, data):
        """
        See TagSerializer.validate().
        """

        if (data['part_of'] is not None and
            self.instance is not None and
                data['part_of'].pk == self.instance.pk):

            raise serializers.ValidationError(
                {'part_of': "Must not be self"},
            )

        return data


class EntitySerializer(BasicEntitySerializer):
    tags = TagSerializer(many=True, required=False)
    part_of = BasicEntitySerializer()


class WritableProductInventoryIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryId
        fields = [
            'id',
            'value',
            'schema',
            'product',
        ]


class BasicProductInventoryIdSerializer(WritableProductInventoryIdSerializer):
    schema = InventoryIdSchemaSerializer()


class WritableItemInventoryIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInventoryId
        fields = [
            'id',
            'value',
            'schema',
            'item',
        ]


class BasicItemInventoryIdSerializer(WritableItemInventoryIdSerializer):
    schema = InventoryIdSchemaSerializer()


class BasicProductSerializer(serializers.ModelSerializer):
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


class ProductDataSerializer(BasicProductDataSerializer):
    type = DataTypeSerializer()
    product = BasicProductSerializer()


class ProductInventoryIdSerializer(BasicProductInventoryIdSerializer):
    product = BasicProductSerializer()


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

    class Meta(BasicProductSerializer.Meta):
        pass


class BasicItemSerializer(serializers.ModelSerializer):
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
    item = BasicItemSerializer()

    class Meta:
        model = ItemData
        fields = [
            'id',
            'value',
            'type',
            'item',
        ]


class ItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    belongs_to = EntitySerializer(required=False)
    product = ProductSerializer()
    target_location = LocationSerializer(required=False)
    actual_location = LocationSerializer(required=False)

    itemdata_set = BasicItemDataSerializer(
        many=True,
        required=False,
    )

    iteminventoryid_set = BasicItemInventoryIdSerializer(
        many=True,
        required=False
    )

    class Meta(BasicItemSerializer.Meta):
        pass


class ItemInventoryIdSerializer(BasicItemInventoryIdSerializer):
    item = BasicItemSerializer


class BasicOverlayItemSerializer(WritableOverlayItemSerializer):
    item = BasicItemSerializer()
    target_item = BasicItemSerializer()
    target_location = LocationSerializer()


class OverlaySerializer(BasicOverlaySerializer):
    parent = BasicOverlaySerializer()
    overlayitem_set = BasicOverlayItemSerializer(many=True)


class OverlayItemSerializer(BasicOverlayItemSerializer):
    overlay = BasicOverlaySerializer()
