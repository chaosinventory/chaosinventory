from rest_framework import viewsets

from ..models import (
    DataType, Entity, InventoryIdSchema, Item, ItemInventoryId, Location,
    LocationData, Product, ProductInventoryId, Tag,
)
from ..serializers import (
    DataTypeSerializer, EntitySerializer, InventoryIdSchemaSerializer,
    ItemInventoryIdSerializer, ItemSerializer, LocationDataSerializer,
    LocationSerializer, ProductInventoryIdSerializer, ProductSerializer,
    TagSerializer,
)


class InventoryIdSchemaViewSet(viewsets.ModelViewSet):
    queryset = InventoryIdSchema.objects.all()
    serializer_class = InventoryIdSchemaSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DataTypeViewSet(viewsets.ModelViewSet):
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer


class LocationDataViewset(viewsets.ModelViewSet):
    queryset = LocationData.objects.all()
    serializer_class = LocationDataSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ProductInventoryIdViewSet(viewsets.ModelViewSet):
    queryset = ProductInventoryId.objects.all()
    serializer_class = ProductInventoryIdSerializer


class ItemInventoryIdViewSet(viewsets.ModelViewSet):
    queryset = ItemInventoryId.objects.all()
    serializer_class = ItemInventoryIdSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
