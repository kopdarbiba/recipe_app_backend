from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import Unit

class UnitModelTestCase(TestCase):

    def setUp(self):
        self.unit_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c",
            "type_shoping_valid": True
        }

    def assertUnitAttributes(self, unit, expected_en, expected_lv, expected_ru, expected_type_shoping_valid):
        self.assertEqual(unit.name_en, expected_en)
        self.assertEqual(unit.name_lv, expected_lv)
        self.assertEqual(unit.name_ru, expected_ru)
        self.assertEqual(unit.type_shoping_valid, expected_type_shoping_valid)

    def test_create_unit(self):
        unit = Unit.objects.create(**self.unit_data)
        self.assertEqual(Unit.objects.count(), 1)
        self.assertUnitAttributes(unit, "a", "b", "c", True)

    def test_str_representation(self):
        unit = Unit.objects.create(**self.unit_data)
        self.assertEqual(str(unit), "a | b")

    def test_unique_constraint(self):
        Unit.objects.create(**self.unit_data)
        with self.assertRaises(IntegrityError):
            Unit.objects.create(name_en="a", name_lv="b", name_ru="c", type_shoping_valid=True)

    def test_type_shoping_valid_null(self):
        unit_data = self.unit_data.copy()
        unit_data["type_shoping_valid"] = None
        unit = Unit.objects.create(**unit_data)
        self.assertUnitAttributes(unit, "a", "b", "c", None)
