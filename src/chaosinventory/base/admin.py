from django.contrib import admin  # noqa

from .models import (
    Tag, DataType, EntityData, LocationData, ProductData, ProductInventoryId,
    ItemData, ItemInventoryId, Entity, Location, Product, Item, InventoryIdSchema,
    Overlay, OverlayItem,
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(EntityData)
class EntityDataAdmin(admin.ModelAdmin):
    pass

@admin.register(LocationData)
class LocationDataAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductData)
class ProductDataAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductInventoryId)
class ProductInventoryIdAdmin(admin.ModelAdmin):
    pass

@admin.register(ItemData)
class ItemDataAdmin(admin.ModelAdmin):
    pass

@admin.register(ItemInventoryId)
class ItemInventoryIdAdmin(admin.ModelAdmin):
    pass

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(InventoryIdSchema)
class InventoryIdSchemaAdmin(admin.ModelAdmin):
    pass

@admin.register(Overlay)
class OverlayAdmin(admin.ModelAdmin):
    pass

@admin.register(OverlayItem)
class OverlayItemAdmin(admin.ModelAdmin):
    pass
