from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import Equipment

class EquipmentModelTestCase(TestCase):

    def setUp(self):
        self.equipment_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertEquipmentAttributes(self, equipment, expected_en, expected_lv, expected_ru):
        self.assertEqual(equipment.name_en, expected_en)
        self.assertEqual(equipment.name_lv, expected_lv)
        self.assertEqual(equipment.name_ru, expected_ru)

    def test_create_equipment(self):
        equipment = Equipment.objects.create(**self.equipment_data)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEquipmentAttributes(equipment, "a", "b", "c")

    def test_str_representation(self):
        equipment = Equipment.objects.create(**self.equipment_data)
        self.assertEqual(str(equipment), "a | b")

    def test_unique_constraint(self):
        Equipment.objects.create(**self.equipment_data)
        with self.assertRaises(IntegrityError):
            Equipment.objects.create(name_en="a", name_lv="b", name_ru="c")
