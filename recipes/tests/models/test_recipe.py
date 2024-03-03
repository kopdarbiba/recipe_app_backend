from decimal import Decimal
from django.test import TestCase
from recipes.models import Recipe
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


    def setUp_three_recipes(self):
        three_recipes = [
            self.recipe,
            RecipeFactory(),
            RecipeFactory()
        ]
        RecipeIngredientFactory(recipe=three_recipes[1], quantity=1, ingredient__price=2.00)
        RecipeIngredientFactory(recipe=three_recipes[2], quantity=2, ingredient__price=2.50)
        return three_recipes

    
    def test_recipe_filter_by_price_returns_all_if_price_not_set(self):
        """WORKS filter_by_price should return all 3 objects"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price()
        self.assertEqual(queryset.count(), len(self.three_recipes))

    def test_recipe_filter_by_price_if_min_price_set_to_2(self):
        """WORKS filter_by_price should return 1 object with a price '5.00'"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(min_price=3)
        self.assertEqual(1, queryset.count())
        self.assertEqual(queryset[0].price, self.three_recipes[2].price)

    def test_recipe_filter_by_price_if_min_price_set_to_1(self):
        """filter_by_price should return 2 objects with prices '2.00' and '5.00'"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(min_price=2.00)
        prices = {recipe.price for recipe in queryset}
        print('if_min_price_set_to_1:')
        print(queryset.count())
        print(prices)

        self.assertTrue('5.00' in prices)
        self.assertTrue('2.00' in prices)
        self.assertEqual(2, queryset.count())

    def test_recipe_filter_by_price_if_min_price_set_to_0(self):
        """WORKS filter_by_price should return all 3 objects"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(min_price=0.00)
        self.assertEqual(queryset.count(), len(self.three_recipes))

    def test_recipe_filter_by_price_if_max_price_set_to_05(self):
        """filter_by_price should return 1 object with a price '0.00'"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(max_price=0.5)
        prices = {recipe.price for recipe in queryset}
        print('if_max_price_set_to_05:')
        print(prices)
        self.assertEqual(1, queryset.count())
        self.assertEqual(queryset[0].price, self.three_recipes[0].price)

    def test_recipe_filter_by_price_if_max_price_set_to_1(self):
        """filter_by_price should return 1 object with a price '0.00'"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(max_price=1)
        prices = {recipe.price for recipe in queryset}
        print('if_max_price_set_to_1:')
        print(prices)
        self.assertEqual(1, queryset.count())
        self.assertEqual(queryset[0].price, self.three_recipes[0].price)

    def test_recipe_filter_by_price_if_max_price_set_to_0(self):
        """filter_by_price should return 1 object with a price '0.00'"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(max_price=0.00)
        prices = {recipe.price for recipe in queryset}
        print('if_max_price_set_to_0:')
        print(prices)
        self.assertEqual(1, queryset.count())
        self.assertEqual(queryset[0].price, self.three_recipes[0].price)

    def test_recipe_filter_by_price_if_max_price_set_to_3(self):
        """filter_by_price should return 2 object with a price '0.00 and '2.00'"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(max_price=3.00)
        prices = {recipe.price for recipe in queryset}
        print('if_max_price_set_to_3:')
        print(prices)
        self.assertTrue('0.00' in prices)
        self.assertTrue('2.00' in prices)
        self.assertEqual(2, queryset.count())

    def test_recipe_filter_by_price_if_min_price_1_max_price_set_to_3(self):
        """WORKS filter_by_price should return 1 object with a price '2.00'"""
        self.three_recipes = self.setUp_three_recipes()
        queryset = Recipe.filter_by_price(min_price=1.00, max_price=3.00)
        prices = {recipe.price for recipe in queryset}
        print('if_min_price_1_max_price_set_to_3:')
        print(prices)
        self.assertEqual(1, queryset.count())
        self.assertEqual(queryset[0].price, self.three_recipes[1].price)