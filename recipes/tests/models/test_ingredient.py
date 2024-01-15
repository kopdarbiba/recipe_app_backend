from django.test import TestCase
from decimal import Decimal
from django.db.utils import IntegrityError
from recipes.models import Ingredient

class IngredientModelTestCase(TestCase):

    def setUp(self):
        self.ingredient_data = {
            "allergen": None,
            "category": None,
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c",
            "price": Decimal('72.90')
        }

    def assertIngredientAttributes(self, ingredient, expected_en, expected_lv, expected_ru, expected_price):
        self.assertEqual(ingredient.allergen, None)
        self.assertEqual(ingredient.category, None)
        self.assertEqual(ingredient.name_en, expected_en)
        self.assertEqual(ingredient.name_lv, expected_lv)
        self.assertEqual(ingredient.name_ru, expected_ru)
        self.assertEqual(ingredient.price, expected_price)

    def test_create_ingredient(self):
        ingredient = Ingredient.objects.create(**self.ingredient_data)
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertIngredientAttributes(ingredient, "a", "b", "c", Decimal('72.90'))

    def test_str_representation(self):
        ingredient = Ingredient.objects.create(**self.ingredient_data)
        self.assertEqual(str(ingredient), "a | b | 72.90")

    def test_unique_constraint(self):
        Ingredient.objects.create(**self.ingredient_data)
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name_en="a", name_lv="b", name_ru="c")

    def test_ingredients_price(self):
        ingredient = Ingredient.objects.create(**self.ingredient_data)
        self.assertEqual(ingredient.price, Decimal('72.90'))
