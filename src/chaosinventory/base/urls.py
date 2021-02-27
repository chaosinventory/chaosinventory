from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import api, index

router = DefaultRouter()
router.register(r'tag', api.TagViewSet)
router.register(r'datatype', api.DataTypeViewSet)
router.register(r'locationdata', api.LocationDataViewset)
router.register(r'entity', api.EntityViewSet)
router.register(r'location', api.LocationViewSet)
router.register(r'product', api.ProductViewSet)
router.register(r'item', api.ItemViewSet)

urlpatterns = [
    path('', index),
    path('api/', include(router.urls))
]
