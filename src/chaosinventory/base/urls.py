from django.conf import settings
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import api, app, index

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
    re_path(r'^app/(?P<path>.*)$', app, {"document_root": settings.APP_ROOT}),
    path('api/', include(router.urls))
]
