from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import api, index

router = DefaultRouter()

router.register(r'item', api.ItemViewSet)
router.register(r'itemdata', api.ItemDataViewSet)
router.register(r'iteminventoryid', api.ItemInventoryIdViewSet)

router.register(r'product', api.ProductViewSet)
router.register(r'productdata', api.ProductDataViewSet)
router.register(r'productinventoryid', api.ProductInventoryIdViewSet)

router.register(r'location', api.LocationViewSet)
router.register(r'locationdata', api.LocationDataViewSet)

router.register(r'entity', api.EntityViewSet)

router.register(r'overlay', api.OverlayViewSet)
router.register(r'overlayitem', api.OverlayItemViewSet)

router.register(r'tag', api.TagViewSet)
router.register(r'datatype', api.DataTypeViewSet)
router.register(r'inventoryidschema', api.InventoryIdSchemaViewSet)

urlpatterns = [
    path('', index),
    path('api/', include(router.urls))
]
