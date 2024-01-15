from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import IngredientCategory

class IngredientCategoryModelTestCase(TestCase):

    def setUp(self):
        self.ingredient_category_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertIngredientCategoryAttributes(self, ingredient_category, expected_en, expected_lv, expected_ru):
        self.assertEqual(ingredient_category.name_en, expected_en)
        self.assertEqual(ingredient_category.name_lv, expected_lv)
        self.assertEqual(ingredient_category.name_ru, expected_ru)

    def test_create_ingredient_category(self):
        ingredient_category = IngredientCategory.objects.create(**self.ingredient_category_data)
        self.assertEqual(IngredientCategory.objects.count(), 1)
        self.assertIngredientCategoryAttributes(ingredient_category, "a", "b", "c")

    def test_str_representation(self):
        ingredient_category = IngredientCategory.objects.create(**self.ingredient_category_data)
        self.assertEqual(str(ingredient_category), "a | b")

    def test_unique_constraint(self):
        IngredientCategory.objects.create(**self.ingredient_category_data)
        with self.assertRaises(IntegrityError):
            IngredientCategory.objects.create(name_en="a", name_lv="b", name_ru="c")
