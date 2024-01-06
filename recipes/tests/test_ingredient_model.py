
from django.test import TestCase
from recipes.models import Ingredient
from recipes.tests.test_setup import create_test_data



class IngredientModelTestCase(TestCase):
    def setUp(self) -> None:
        create_test_data()


    def test_ingredients_price(self):
        ingredient = Ingredient.objects.get(name_en='Garlic')
        self.assertEqual(ingredient.price, 3)
