from decimal import Decimal
from django.test import TestCase
from recipes.models import Recipe, RecipeIngredient


class RecipeModelTestCase(TestCase):
    fixtures = ['recipes/fixtures/recipes_data.json']
    def setUp(self) -> None:
        None

    def test_recipe_count(self):
        self.assertEqual(Recipe.objects.count(), 11)

    def test_dietary_preferences_count(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        self.assertEqual(recipe.dietary_preferences.count(), 1)

    def test_equipment_count(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        self.assertEqual(recipe.equipment.count(), 1)

    def test_cooking_methods_count(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        self.assertEqual(recipe.cooking_methods.count(), 1)

    def test_recipe_ingredients_count(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        self.assertEqual(recipe.recipe_ingredients.count(), 9)

    def test_cooking_step_instructions_count(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        self.assertEqual(recipe.instructions.count(), 5)

    def test_recipe_ingredients_quantity(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        recipe_ingredient = RecipeIngredient.objects.get(recipe=recipe, ingredient__name_en='pork')
        self.assertEqual(recipe_ingredient.quantity, 1)

    def test_recipe_ingredients_unit(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        recipe_ingredient = RecipeIngredient.objects.get(recipe=recipe, ingredient__name_en='pork')
        self.assertEqual(recipe_ingredient.unit.name_en, 'kilogram (kg)')

    def test_recipe_price(self):
        recipe = Recipe.objects.get(title__name_en='pork meatballs')
        
        # Set the precision to two decimal places for comparison
        expected_price = Decimal('14056.76').quantize(Decimal('0.00'))

        self.assertEqual(recipe.get_price(), expected_price)
