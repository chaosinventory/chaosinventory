from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import (
    DataType, Entity, InventoryIdSchema, Item, ItemData, ItemInventoryId,
    Location, LocationData, Overlay, OverlayItem, Product, ProductData,
    ProductInventoryId, Tag,
)
from ..serializers import (
    DataTypeSerializer, EntitySerializer, InventoryIdSchemaSerializer,
    ItemDataSerializer, ItemInventoryIdSerializer, ItemSerializer,
    LocationDataSerializer, LocationSerializer, OverlayItemSerializer,
    OverlaySerializer, ProductDataSerializer, ProductInventoryIdSerializer,
    ProductSerializer, TagSerializer,
)


class InventoryIdSchemaViewSet(viewsets.ModelViewSet):
    queryset = InventoryIdSchema.objects.all()
    serializer_class = InventoryIdSchemaSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DataTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer


class LocationDataViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LocationData.objects.all()
    serializer_class = LocationDataSerializer


class ItemDataViewset(viewsets.ModelViewSet):
    queryset = ItemData.objects.all()
    serializer_class = ItemDataSerializer


class ProductDataViewset(viewsets.ModelViewSet):
    queryset = ProductData.objects.all()
    serializer_class = ProductDataSerializer


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class OverlayViewset(viewsets.ModelViewSet):
    queryset = Overlay.objects.all()
    serializer_class = OverlaySerializer


class OverlayItemViewset(viewsets.ModelViewSet):
    queryset = OverlayItem.objects.all()
    serializer_class = OverlayItemSerializer


class EntityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ProductInventoryIdViewSet(viewsets.ModelViewSet):
    queryset = ProductInventoryId.objects.all()
    serializer_class = ProductInventoryIdSerializer


class ItemInventoryIdViewSet(viewsets.ModelViewSet):
    queryset = ItemInventoryId.objects.all()
    serializer_class = ItemInventoryIdSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
