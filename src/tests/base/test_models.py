from string import ascii_lowercase

from django.core.exceptions import ValidationError
from django.test import TestCase

from chaosinventory.base.models import (
    Entity, Item, Location, Overlay, Product, Tag,
)


class TagTestCase(TestCase):
    def test_tag_parent_not_direct_self(self):
        tag_a: Tag = Tag.objects.create(name='TagA')
        tag_b: Tag = Tag.objects.create(name='TagB')
        self.assertTrue(tag_a.parent_is_parent(tag_a))
        self.assertFalse(tag_a.parent_is_parent(tag_b))
        self.assertFalse(tag_a.parent_is_parent(None))
        self.assertEqual(tag_a.parent_is_parent(tag_b), False)
        with self.assertRaises(ValidationError):
            tag_a.parent = tag_a
            tag_a.clean()

    def test_tag_parent_not_parent_self(self):
        tags = []
        for c in ascii_lowercase:
            tag: Tag = Tag.objects.create(name=f'Tag {c}')
            if len(tags) >= 1:
                tag.parent = tags[-1]
                tag.save()
            tags.append(tag)

        self.assertTrue(tags[-1].parent_is_parent(tags[0]))
        self.assertFalse(tags[0].parent_is_parent(tags[-1]))
        with self.assertRaises(ValidationError):
            tags[0].parent = tags[-1]
            tags[0].clean()


class EntityTestCase(TestCase):
    def test_entity_parent_not_direct_self(self):
        entity_a: Entity = Entity.objects.create(name='Entity A')
        entity_b: Entity = Entity.objects.create(name='Entity B')
        self.assertTrue(entity_a.part_of_is_parent(entity_a))
        self.assertFalse(entity_a.part_of_is_parent(entity_b))
        self.assertFalse(entity_a.part_of_is_parent(None))
        self.assertEqual(entity_a.part_of_is_parent(entity_b), False)
        with self.assertRaises(ValidationError):
            entity_a.part_of = entity_a
            entity_a.clean()

    def test_entity_parent_not_parent_self(self):
        entities = []
        for c in ascii_lowercase:
            entity: Entity = Entity.objects.create(name=f'Entity {c}')
            if len(entities) >= 1:
                entity.part_of = entities[-1]
                entity.save()
            entities.append(entity)

        self.assertTrue(entities[-1].part_of_is_parent(entities[0]))
        self.assertFalse(entities[0].part_of_is_parent(entities[-1]))
        self.assertFalse(entities[-10].part_of_is_parent(entities[-5]))
        self.assertTrue(entities[-5].part_of_is_parent(entities[-10]))
        with self.assertRaises(ValidationError):
            entities[0].part_of = entities[-1]
            entities[0].clean()


class LocationTestCase(TestCase):
    def test_parent_not_parent_direct(self):
        location_a: Location = Location.objects.create(name='Location A',)
        location_b: Location = Location.objects.create(name='Location B',)
        self.assertTrue(location_a.in_location_is_parent(location_a))
        self.assertFalse(location_a.in_location_is_parent(location_b))
        self.assertFalse(location_a.in_location_is_parent(None))
        self.assertEqual(location_a.in_location_is_parent(location_b), False)
        with self.assertRaises(ValidationError):
            location_a.in_location = location_a
            location_a.clean()

    def test_parent_not_parent_self(self):
        locations = []
        for c in ascii_lowercase:
            location: Location = Location.objects.create(name=f'Entity {c}')
            if len(locations) >= 1:
                location.in_location = locations[-1]
                location.save()
            locations.append(location)

        self.assertTrue(locations[-1].in_location_is_parent(locations[0]))
        self.assertFalse(locations[0].in_location_is_parent(locations[-1]))
        self.assertFalse(locations[-10].in_location_is_parent(locations[-5]))
        self.assertTrue(locations[-5].in_location_is_parent(locations[-10]))
        with self.assertRaises(ValidationError):
            locations[0].in_location = locations[-1]
            locations[0].clean()


class ItemTestCase(TestCase):
    def setUp(self) -> None:
        self.product: Product = Product.objects.create(name="Test Product")
        self.item_a: Item = Item.objects.create(name='Item A', product=self.product)
        self.item_b: Item = Item.objects.create(name='Item B', product=self.product)

    def test_target_is_parent_direct(self):
        self.assertTrue(self.item_a.target_item_is_parent(self.item_a))
        self.assertFalse(self.item_a.target_item_is_parent(self.item_b))
        self.assertFalse(self.item_a.target_item_is_parent(None))
        self.assertEqual(self.item_a.target_item_is_parent(self.item_b), False)
        with self.assertRaises(ValidationError):
            self.item_a.target_item = self.item_a
            self.item_a.clean()
        self.item_a.target_item = None

    def test_actual_is_parent_direct(self):
        self.assertTrue(self.item_a.actual_item_is_parent(self.item_a))
        self.assertFalse(self.item_a.actual_item_is_parent(self.item_b))
        self.assertFalse(self.item_a.actual_item_is_parent(None))
        self.assertEqual(self.item_a.actual_item_is_parent(self.item_b), False)
        with self.assertRaises(ValidationError):
            self.item_a.actual_item = self.item_a
            self.item_a.clean()
        self.item_a.actual_item = None

    def test_target_is_parent_self(self):
        items = []
        for c in ascii_lowercase:
            item: Item = Item.objects.create(name=f'Entity {c}', product=self.product)
            if len(items) >= 1:
                item.target_item = items[-1]
                item.save()
            items.append(item)

        self.assertTrue(items[-1].target_item_is_parent(items[0]))
        self.assertFalse(items[0].target_item_is_parent(items[-1]))
        self.assertFalse(items[-10].target_item_is_parent(items[-5]))
        self.assertTrue(items[-5].target_item_is_parent(items[-10]))
        with self.assertRaises(ValidationError):
            items[0].target_item = items[-1]
            items[0].clean()

    def test_actual_is_parent_self(self):
        items = []
        for c in ascii_lowercase:
            item: Item = Item.objects.create(name=f'Entity {c}', product=self.product)
            if len(items) >= 1:
                item.actual_item = items[-1]
                item.save()
            items.append(item)

        self.assertTrue(items[-1].actual_item_is_parent(items[0]))
        self.assertFalse(items[0].actual_item_is_parent(items[-1]))
        self.assertFalse(items[-10].actual_item_is_parent(items[-5]))
        self.assertTrue(items[-5].actual_item_is_parent(items[-10]))
        with self.assertRaises(ValidationError):
            items[0].actual_item = items[-1]
            items[0].clean()

    def test_target_actual_exclusive(self):
        location: Location = Location.objects.create(name='Location')
        with self.assertRaisesMessage(
            ValidationError,
            'Actual location and item are mutually exclusive',
        ):
            self.item_a.actual_item = self.item_b
            self.item_a.actual_location = location
            self.item_a.clean()

        self.item_a.actual_item = None
        self.item_a.actual_location = None

        with self.assertRaisesMessage(
            ValidationError,
            'Target location and item are mutually exclusive',
        ):
            self.item_a.target_item = self.item_b
            self.item_a.target_location = location
            self.item_a.clean()

        self.item_a.target_item = None
        self.item_a.target_location = None


# noinspection DuplicatedCode
class OverlayTestCase(TestCase):
    def test_parent_not_parent_direct(self):
        overlay_a: Overlay = Overlay.objects.create(name='Overlay A', active=True)
        overlay_b: Overlay = Overlay.objects.create(name='Overlay B', active=True)

        self.assertTrue(overlay_a.parent_is_parent(overlay_a))
        self.assertFalse(overlay_a.parent_is_parent(overlay_b))
        self.assertFalse(overlay_a.parent_is_parent(None))
        self.assertEqual(overlay_a.parent_is_parent(overlay_b), False)
        with self.assertRaises(ValidationError):
            overlay_a.parent = overlay_a
            overlay_a.clean()

    def test_parent_is_parent_self(self):
        overlays = []
        for c in ascii_lowercase:
            overlay: Overlay = Overlay.objects.create(name=f'Tag {c}', active=True)
            if len(overlays) >= 1:
                overlay.parent = overlays[-1]
                overlay.save()
            overlays.append(overlay)

        self.assertTrue(overlays[-1].parent_is_parent(overlays[0]))
        self.assertFalse(overlays[0].parent_is_parent(overlays[-1]))
        with self.assertRaises(ValidationError):
            overlays[0].parent = overlays[-1]
            overlays[0].clean()
