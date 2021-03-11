from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class CommonModel(models.Model):
    name = models.CharField(
        max_length=255
    )

    note = models.TextField(
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CommonTypeData(models.Model):
    value = models.TextField()

    type = models.ForeignKey(
        'DataType',
        on_delete=models.RESTRICT
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.type.name + ": " + self.value[:25]


class CommonInventoryId(models.Model):
    schema = models.ForeignKey(
        'InventoryIdSchema',
        on_delete=models.RESTRICT,
    )

    value = models.CharField(
        max_length=255,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.schema.name + ": " + self.value[:25]


class Tag(models.Model):
    name = models.CharField(
        max_length=255
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class DataType(CommonModel):
    pass


class EntityData(CommonTypeData):
    entity = models.ForeignKey(
        'Entity',
        on_delete=models.CASCADE,
    )


class LocationData(CommonTypeData):
    location = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
    )


class ProductData(CommonTypeData):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )


class ProductInventoryId(CommonInventoryId):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )

    class Meta:
        pass


class ItemData(CommonTypeData):
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
    )


class ItemInventoryId(CommonInventoryId):
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
    )

    class Meta:
        pass


class Entity(CommonModel):
    part_of = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        'Tag',
        null=True,
        blank=True,
    )


class Location(CommonModel):
    in_location = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    belongs_to = models.ForeignKey(
        'Entity',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        'Tag',
        null=True,
        blank=True,
    )


class Product(CommonModel):
    tags = models.ManyToManyField(
        'Tag',
        null=True,
        blank=True,
    )


class Item(CommonModel):
    amount = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    belongs_to = models.ForeignKey(
        'Entity',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    target_location = models.ForeignKey(
        'Location',
        on_delete=models.RESTRICT,
        related_name='target_contents',
        null=True,
        blank=True,
    )

    actual_location = models.ForeignKey(
        'Location',
        on_delete=models.RESTRICT,
        related_name='actual_contents',
        null=True,
        blank=True,
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.RESTRICT
    )

    target_item = models.ForeignKey(
        'Item',
        on_delete=models.RESTRICT,
        related_name='target_contents',
        null=True,
        blank=True,
    )

    actual_item = models.ForeignKey(
        'Item',
        on_delete=models.RESTRICT,
        related_name='actual_contents',
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        'Tag',
        null=True,
        blank=True,
    )

    def clean(self):
        if (self.target_location and self.target_item):
            raise ValidationError("Target location and item are mutually exclusive")
        if (self.actual_location and self.actual_item):
            raise ValidationError("Actual location and item are mutually exclusive")


class InventoryIdSchema(CommonModel):
    pass


class Overlay(CommonModel):
    active = models.BooleanField()

    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        related_name='children',
        null=True,
        blank=True,
    )


class OverlayItem(models.Model):
    overlay = models.ForeignKey(
        'Overlay',
        on_delete=models.RESTRICT,
    )

    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
    )

    target_item = models.ForeignKey(
        'Item',
        on_delete=models.RESTRICT,
        related_name='overlay_contents',
        null=True,
        blank=True,
    )

    target_location = models.ForeignKey(
        'Location',
        on_delete=models.RESTRICT,
        related_name='overlay_contents',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.overlay.name + ": " + self.item.name
