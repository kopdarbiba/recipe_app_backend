from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import Allergen

class AllergenModelTestCase(TestCase):

    def setUp(self):
        self.allergen_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertAllergenAttributes(self, allergen, expected_en, expected_lv, expected_ru):
        self.assertEqual(allergen.name_en, expected_en)
        self.assertEqual(allergen.name_lv, expected_lv)
        self.assertEqual(allergen.name_ru, expected_ru)

    def test_create_allergen(self):
        allergen = Allergen.objects.create(**self.allergen_data)
        self.assertEqual(Allergen.objects.count(), 1)
        self.assertAllergenAttributes(allergen, "a", "b", "c")

    def test_str_representation(self):
        allergen = Allergen.objects.create(**self.allergen_data)
        self.assertEqual(str(allergen), "a | b")

    def test_unique_constraint(self):
        Allergen.objects.create(**self.allergen_data)
        with self.assertRaises(IntegrityError):
            Allergen.objects.create(name_en="a", name_lv="b", name_ru="c")
