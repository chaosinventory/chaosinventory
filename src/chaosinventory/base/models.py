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
    value = models.CharField(
        max_length=255,
    )

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
        max_length=255,
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent and self.pk == self.parent.pk:
            raise ValidationError(
                {'parent': 'Must not be self'},
            )


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


class Entity(CommonModel):
    part_of = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        'Tag',
        blank=True,
    )

    def clean(self):
        if self.part_of and self.pk == self.part_of.pk:
            raise ValidationError(
                {'part_of': 'Must not be self'},
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
        blank=True,
    )

    def clean(self):
        if self.in_location and self.pk == self.in_location.pk:
            raise ValidationError(
                {'in_location': 'Must not be self'},
            )


class Product(CommonModel):
    tags = models.ManyToManyField(
        'Tag',
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
        blank=True,
    )

    @property
    def target_parent(self):
        return self.target_item if self.target_item else self.target_location

    @target_parent.setter
    def target_parent(self, new_parent):
        if type(new_parent) is Item:
            self.target_location = None
            self.target_item = new_parent
        else:
            self.target_item = None
            self.target_location = new_parent

    @property
    def actual_parent(self):
        return self.actual_item if self.actual_item else self.actual_location

    @actual_parent.setter
    def actual_parent(self, new_parent):
        if type(new_parent) is Item:
            self.actual_location = None
            self.actual_item = new_parent
        else:
            self.actual_item = None
            self.actual_location = new_parent

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

    def clean(self):
        if self.parent and self.pk == self.parent.pk:
            raise ValidationError(
                {'parent': 'A object can not be its own parent'},
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
