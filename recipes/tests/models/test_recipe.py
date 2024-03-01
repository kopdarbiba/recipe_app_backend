from decimal import Decimal
from django.test import TestCase
from recipes.tests.factory import RecipeFactory, RecipeIngredientFactory

class RecipeModelTestCase(TestCase):
    def setUp(self) -> None:
        self.recipe = RecipeFactory()

    def test_recipe_str_representation(self):
        expected_str = f"model Recipe: {self.recipe.title}"
        self.assertEqual(str(self.recipe), expected_str)

    def test_recipe_total_price_with_no_ingredients(self):
        total_price = self.recipe.get_recipe_total_price()
        self.assertEqual(total_price, 0)

    def test_recipe_total_price_with_existing_ingredients(self):
        recipe_ingredient1 = RecipeIngredientFactory(recipe=self.recipe, quantity=1, ingredient__price=Decimal('3.53'))
        recipe_ingredient2 = RecipeIngredientFactory(recipe=self.recipe, quantity=1, ingredient__price=Decimal('2.15'))

        total_price = self.recipe.get_recipe_total_price()
        v1 = recipe_ingredient1.quantity * recipe_ingredient1.ingredient.price
        v2 = recipe_ingredient2.quantity * recipe_ingredient2.ingredient.price

        expected_total_price = v1 + v2
        self.assertEqual(total_price, expected_total_price)
