from django.test import TestCase
from recipes.models import Recipe, Ingredient, RecipeIngredient
from recipes.tests.test_setup import create_test_data



class YourModelTestCase(TestCase):
    def setUp(self) -> None:
        create_test_data()
    
    def test_dietary_preferences_count(self):
        recipe = Recipe.objects.get(title__name_en='title_2')
        self.assertEqual(recipe.dietary_preferences.count(), 1)

    def test_equipment_count(self):
        recipe = Recipe.objects.get(title__name_en='title_1')
        self.assertEqual(recipe.equipment.count(), 2)

    def test_cooking_methods_count(self):
        recipe = Recipe.objects.get(title__name_en='title_1')
        self.assertEqual(recipe.cooking_methods.count(), 2)

    def test_recipe_ingredients_count(self):
        recipe = Recipe.objects.get(title__name_en='title_1')
        self.assertEqual(recipe.recipe_ingredients.count(), 2)

    def test_cooking_step_instructions_count(self):
        recipe = Recipe.objects.get(title__name_en='title_1')
        self.assertEqual(recipe.instructions.count(), 3)

    def test_recipe_ingredients_quantity(self):
        recipe = Recipe.objects.get(title__name_en='title_1')
        recipe_ingredient = RecipeIngredient.objects.get(recipe=recipe, ingredient__name_en='Garlic')
        self.assertEqual(recipe_ingredient.quantity, 1)

    def test_recipe_ingredients_unit(self):
        recipe = Recipe.objects.get(title__name_en='title_1')
        recipe_ingredient = RecipeIngredient.objects.get(recipe=recipe, ingredient__name_en='Garlic')
        self.assertEqual(recipe_ingredient.unit.name_en, 'kg')

    def test_ingredients_price(self):
        ingredient = Ingredient.objects.get(name_en='Garlic')
        self.assertEqual(ingredient.price, 3)

    def test_recipe_price(self):
        recipe = Recipe.objects.get(title__name_en='title_1')
        self.assertEqual(recipe.get_price(), 21)
