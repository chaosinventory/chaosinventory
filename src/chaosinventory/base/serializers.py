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


class CommonBasicDataSerializer(serializers.ModelSerializer):
    type_name = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = ProductData
        fields = [
            'id',
            'value',
            'type',
            'type_name',
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


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = [
            'id',
            'name',
            'note'
        ]


class LocationDataSerializer(serializers.ModelSerializer):
    type_name = serializers.ReadOnlyField(source='type.name', read_only=True)

    class Meta:
        model = LocationData
        fields = [
            'id',
            'value',
            'type',
            'type_name',
            'location'
        ]


class ItemDataSerializer(serializers.ModelSerializer):
    type_name = serializers.ReadOnlyField(source='type.name', read_only=True)

    class Meta:
        model = ItemData
        fields = [
            'id',
            'value',
            'type',
            'type_name',
            'item'
        ]


class ProductDataSerializer(serializers.ModelSerializer):
    type_name = serializers.ReadOnlyField(source='type.name', read_only=True)

    class Meta:
        model = ProductData
        fields = [
            'id',
            'value',
            'type',
            'type_name',
            'product'
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
    locationdata_set = BasicLocationDataSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'note',
            'in_location',
            'locationdata_set'
        ]


class OverlaySerializer(serializers.ModelSerializer):
    overlayitem_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
    """
    .. note::

        Currently, entitys can not be created if we use the TagSerializer.
        Thus, all the _set attributes (and all other foreign Keys
        therefore) only consist of the foreign id. This, for now,
        requires multiple requests but we would like tho improve on this
        in the future. A notable exception are all Models with a
        :code:`type`  for which we serialize the :code:`id` and, as
        :code:`type_name` the name of the type. However, **this is not
        consideres stable and will probably change in the (near) future!**

    .. todo::

        Write a custom create method so that we can print out the
        Tag data but also append Tags to newly created entitys
    """
    # tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Entity
        fields = [
            'id',
            'name',
            'note',
            'part_of',  # TODO: Make recursive?
            'tags',
        ]


class BasicProductDataSerializer(CommonBasicDataSerializer):
    class Meta(CommonBasicDataSerializer.Meta):
        model = ProductData


class BasicItemDataSerializer(CommonBasicDataSerializer):
    class Meta(CommonBasicDataSerializer.Meta):
        model = ItemData


class ProductInventoryIdSerializer(CommonBasicInventoryIdSerializer):
    class Meta(CommonBasicInventoryIdSerializer.Meta):
        """
        Originally we tried to do simple inheritance like this:

        .. code-block:: python

            class ProductInventoryIdSerializer(SuperClass):
                class Meta(SuperClass.Meta):
                    fields = SuperClass.Meta.fields
                    fields.append('product')

        and the same for ItemInventoryId. However things broke in
        strange™ ways, since the
        :code:`ItemInventoryIdSerializer.Meta.Fields` contained
        :code:`product` since it was inherrited from
        :code:`ProductInventoryIdSerializer`. Because of this behaviour,
        and our motivation to keep everything inherited, we had to do it
        this way...
        """
        model = ProductInventoryId
        fields = []
        fields.extend(CommonBasicInventoryIdSerializer.Meta.fields)
        fields.append('product')


class ItemInventoryIdSerializer(CommonBasicInventoryIdSerializer):
    class Meta(CommonBasicInventoryIdSerializer.Meta):
        model = ItemInventoryId
        fields = []
        fields.extend(CommonBasicInventoryIdSerializer.Meta.fields)
        fields.append('item')


class ProductSerializer(serializers.ModelSerializer):
    # Same issue as with EntitySerializer
    # TODO: custom create method
    # tags = TagSerializer(many=True, required=False)

    # productdata_set = BasicProductDataSerializer(
    #     many=True,
    #     required=False
    # )
    # productinventoryid_set = ProductInventoryIdSerializer(
    #     many=True,
    #     required=False
    # )

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
    # Same issue as with EntitySerializer
    # TODO: custom create method
    # tags = TagSerializer(many=True, required=False)
    # belongs_to = EntitySerializer()
    # product = ProductSerializer()
    # target_location = LocationSerializer(required=False)
    # actual_location = LocationSerializer()

    # itemdata_set = BasicItemDataSerializer(
    #     many=True,
    #     required=False
    # )

    # iteminventoryid_set = ItemInventoryIdSerializer(
    #     many=True,
    #     required=False
    # )

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
            'iteminventoryid_set',  # can not yet be created via the API
            'itemdata_set',
            'tags',
        ]
