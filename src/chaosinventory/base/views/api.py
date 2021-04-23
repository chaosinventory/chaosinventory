from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import (
    DataType, Entity, InventoryIdSchema, Item, ItemData, ItemInventoryId,
    Location, LocationData, Overlay, OverlayItem, Product, ProductData,
    ProductInventoryId, Tag,
)
from ..serializers import (
    BasicEntitySerializer, BasicItemDataSerializer, BasicItemSerializer,
    BasicLocationSerializer, BasicOverlaySerializer,
    BasicProductDataSerializer, BasicProductSerializer, BasicTagSerializer,
    DataTypeSerializer, EntitySerializer, InventoryIdSchemaSerializer,
    ItemDataSerializer, ItemInventoryIdSerializer, ItemSerializer,
    LocationDataSerializer, LocationSerializer, OverlayItemSerializer,
    OverlaySerializer, ProductDataSerializer, ProductInventoryIdSerializer,
    ProductSerializer, TagSerializer, WritableItemInventoryIdSerializer,
    WritableLocationDataSerializer, WritableOverlayItemSerializer,
    WritableProductInventoryIdSerializer,
)


class AbstractModelViewSet(viewsets.ModelViewSet):
    """
    A wrapper class we can reuse for our recursive serializers
    """

    writable_serializer_class = None

    def create(self, request: Request, **kwargs):
        """
        Create a Model instance.
        """
        serializer = self.writable_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request: Request, *args, **kwargs):
        """
        Update a Model instance.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.writable_serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_writable_serializer(self, *args, **kwargs):
        """
        Return the class to use for the serializer. Basically copied from
        `rest_framework.viewsets.ViewSetMixin`, thus the two-function structure.

        In the end, it returns the serializer specified in self.writable_serializer_class.
        """
        writable_serializer_class = self.get_writable_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return writable_serializer_class(*args, **kwargs)

    def get_writable_serializer_class(self):
        assert self.writable_serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or overwrite the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.writable_serializer_class


class InventoryIdSchemaViewSet(viewsets.ModelViewSet):
    queryset = InventoryIdSchema.objects.all()
    serializer_class = InventoryIdSchemaSerializer


class TagViewSet(AbstractModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    writable_serializer_class = BasicTagSerializer


class DataTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer


class LocationDataViewSet(AbstractModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LocationData.objects.all()
    serializer_class = LocationDataSerializer
    writable_serializer_class = WritableLocationDataSerializer


class ItemDataViewSet(AbstractModelViewSet):
    queryset = ItemData.objects.all()
    serializer_class = ItemDataSerializer
    writable_serializer_class = BasicItemDataSerializer


class ProductDataViewSet(AbstractModelViewSet):
    queryset = ProductData.objects.all()
    serializer_class = ProductDataSerializer
    writable_serializer_class = BasicProductDataSerializer


class LocationViewSet(AbstractModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    writable_serializer_class = BasicLocationSerializer


class OverlayViewSet(AbstractModelViewSet):
    queryset = Overlay.objects.all()
    serializer_class = OverlaySerializer
    writable_serializer_class = BasicOverlaySerializer


class OverlayItemViewSet(AbstractModelViewSet):
    queryset = OverlayItem.objects.all()
    serializer_class = OverlayItemSerializer
    writable_serializer_class = WritableOverlayItemSerializer


class EntityViewSet(AbstractModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    writable_serializer_class = BasicEntitySerializer


class ProductInventoryIdViewSet(AbstractModelViewSet):
    queryset = ProductInventoryId.objects.all()
    serializer_class = ProductInventoryIdSerializer
    writable_serializer_class = WritableProductInventoryIdSerializer


class ItemInventoryIdViewSet(AbstractModelViewSet):
    queryset = ItemInventoryId.objects.all()
    serializer_class = ItemInventoryIdSerializer
    writable_serializer_class = WritableItemInventoryIdSerializer


class ProductViewSet(AbstractModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    writable_serializer_class = BasicProductSerializer


class ItemViewSet(AbstractModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    writable_serializer_class = BasicItemSerializer
