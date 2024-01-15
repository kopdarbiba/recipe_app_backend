from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import CookingMethod

class CookingMethodModelTestCase(TestCase):

    def setUp(self):
        self.cooking_method_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertCookingMethodAttributes(self, cooking_method, expected_en, expected_lv, expected_ru):
        self.assertEqual(cooking_method.name_en, expected_en)
        self.assertEqual(cooking_method.name_lv, expected_lv)
        self.assertEqual(cooking_method.name_ru, expected_ru)

    def test_create_cooking_method(self):
        cooking_method = CookingMethod.objects.create(**self.cooking_method_data)
        self.assertEqual(CookingMethod.objects.count(), 1)
        self.assertCookingMethodAttributes(cooking_method, "a", "b", "c")

    def test_str_representation(self):
        cooking_method = CookingMethod.objects.create(**self.cooking_method_data)
        self.assertEqual(str(cooking_method), "a | b")

    def test_unique_constraint(self):
        CookingMethod.objects.create(**self.cooking_method_data)
        with self.assertRaises(IntegrityError):
            CookingMethod.objects.create(name_en="a", name_lv="b", name_ru="c")
