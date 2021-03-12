from django.contrib import admin  # noqa

from .models import (
    DataType, Entity, EntityData, InventoryIdSchema, Item, ItemData,
    ItemInventoryId, Location, LocationData, Overlay, OverlayItem, Product,
    ProductData, ProductInventoryId, Tag,
)


class CommonInline(admin.TabularInline):
    extra = 0


class CommonDataInline(CommonInline):
    fields = ('type', 'value',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ("Properties", {
            'fields': ('parent',),
        }),
    )

    search_fields = ('name',)


@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'note',),
        }),
    )

    search_fields = ('name',)


class EntityDataInline(CommonDataInline):
    model = EntityData


class LocationDataInline(CommonDataInline):
    model = LocationData


class ProductDataInline(CommonDataInline):
    model = ProductData


class ProductInventoryIdInline(CommonInline):
    model = ProductInventoryId


class ItemDataInline(CommonDataInline):
    model = ItemData


class ItemInventoryIdInline(CommonInline):
    model = ItemInventoryId


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'note',),
        }),
        ("Ownership", {
            'fields': ('part_of',),
        }),
        ("Tags", {
            'fields': ('tags',),
        }),
    )
    inlines = [
        EntityDataInline,
    ]

    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'note',),
        }),
        ("Location", {
            'fields': ('in_location',),
        }),
        ("Ownership", {
            'fields': ('belongs_to',),
        }),
        ("Tags", {
            'fields': ('tags',),
        }),
    )
    inlines = [
        LocationDataInline,
    ]

    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'note',),
        }),
        ("Tags", {
            'fields': ('tags',),
        }),
    )
    inlines = [
        ProductInventoryIdInline,
        ProductDataInline,
    ]

    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'note',),
        }),
        ("Properties", {
            'fields': ('product', 'amount',),
        }),
        ("Location", {
            'fields': ('target_location', 'actual_location', 'target_item', 'actual_item',),
        }),
        ("Ownership", {
            'fields': ('belongs_to',),
        }),
        ("Tags", {
            'fields': ('tags',),
        }),
    )
    inlines = [
        ItemInventoryIdInline,
        ItemDataInline,
    ]

    list_display = ('name', 'product', 'amount', 'belongs_to')
    list_filter = ('product', 'belongs_to')
    ordering = ('name', )

    search_fields = ('name',)


@admin.register(InventoryIdSchema)
class InventoryIdSchemaAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'note',),
        }),
    )

    search_fields = ('name',)


class OverlayItemInline(CommonInline):
    model = OverlayItem


@admin.register(Overlay)
class OverlayAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'note',),
        }),
        ("Status", {
            'fields': ('active',),
        }),
        ("Properties", {
            'fields': ('parent',),
        }),
    )
    inlines = [
        OverlayItemInline,
    ]

    search_fields = ('name',)
