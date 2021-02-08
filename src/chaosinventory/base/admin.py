from django.contrib import admin  # noqa

from .models import (
    Tag, DataType, EntityData, LocationData, ProductData, ProductInventoryId,
    ItemData, ItemInventoryId, Entity, Location, Product, Item, InventoryIdSchema,
    Overlay, OverlayItem,
)

class CommonInline(admin.TabularInline):
    extra = 0

class CommonDataInline(CommonInline):
    fields = ( 'type', 'value', )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', ),
        }),
        ("Properties", {
            'fields': ( 'parent', ),
        }),
    )

@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', 'note', ),
        }),
    )

class EntityDataInline(CommonDataInline):
    model = EntityData

class LocationDataInline(CommonDataInline):
    model = LocationData

class ProductDataInline(CommonDataInline):
    model = ProductData

@admin.register(ProductInventoryId)
class ProductInventoryIdAdmin(admin.ModelAdmin):
    pass

class ItemDataInline(CommonDataInline):
    model = ItemData

@admin.register(ItemInventoryId)
class ItemInventoryIdAdmin(admin.ModelAdmin):
    pass

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', 'note', ),
        }),
        ("Ownership", {
            'fields': ( 'part_of', ),
        }),
        ("Tags", {
            'fields': ( 'tags', ),
        }),
    )
    inlines = [
        EntityDataInline,
    ]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', 'note', ),
        }),
        ("Location", {
            'fields': ( 'in_location', ),
        }),
        ("Ownership", {
            'fields': ( 'belongs_to', ),
        }),
        ("Tags", {
            'fields': ( 'tags', ),
        }),
    )
    inlines = [
        LocationDataInline,
    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', 'note', ),
        }),
        ("Inventory IDs", {
            'fields': ( 'inventory_id', ),
        }),
        ("Tags", {
            'fields': ( 'tags', ),
        }),
    )
    inlines = [
        ProductDataInline,
    ]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', 'note', ),
        }),
        ("Properties", {
            'fields': ( 'product', 'amount', ),
        }),
        ("Location", {
            'fields': ( 'target_location', 'actual_location', 'target_item', 'actual_item', ),
        }),
        ("Ownership", {
            'fields': ( 'belongs_to', ),
        }),
        ("Inventory IDs", {
            'fields': ( 'inventory_id', ),
        }),
        ("Tags", {
            'fields': ( 'tags', ),
        }),
    )
    inlines = [
        ItemDataInline,
    ]

@admin.register(InventoryIdSchema)
class InventoryIdSchemaAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', 'note', ),
        }),
    )

class OverlayItemInline(CommonInline):
    model = OverlayItem

@admin.register(Overlay)
class OverlayAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'name', 'note', ),
        }),
        ("Status", {
            'fields': ( 'active', ),
        }),
        ("Properties", {
            'fields': ( 'parent', ),
        }),
    )
    inlines = [
        OverlayItemInline,
    ]
