from decimal import Decimal
from django.test import TestCase
from recipes.models import Recipe
from recipes.tests.factory import RecipeFactory, RecipeIngredientFactory

class RecipeModelTestCase(TestCase):
    def setUp(self) -> None:
        self.recipe = RecipeFactory()
        self.prices = [Decimal('0'), Decimal('2.00'), Decimal('2.50')]
        self.total_prices = [Decimal('0'), Decimal('2.00'), Decimal('2.50')]

    def test_recipe_str_representation(self):
        expected_str = f"model Recipe: {self.recipe.title}"
        self.assertEqual(str(self.recipe), expected_str)

    def test_recipe_total_price_with_no_ingredients(self):
        total_price = self.recipe.calculated_total_price
        self.assertEqual(total_price, 0)

    def test_recipe_total_price_with_existing_ingredients(self):
        recipe_ingredient1 = RecipeIngredientFactory(recipe=self.recipe, quantity=1, ingredient__price=Decimal('3.53'))
        recipe_ingredient2 = RecipeIngredientFactory(recipe=self.recipe, quantity=1, ingredient__price=Decimal('2.15'))

        total_price = self.recipe.calculated_total_price
        v1 = recipe_ingredient1.quantity * recipe_ingredient1.ingredient.price
        v2 = recipe_ingredient2.quantity * recipe_ingredient2.ingredient.price

        expected_total_price = v1 + v2
        self.assertEqual(total_price, expected_total_price)


    def setUp_three_recipes(self):
        """Sets up 3 recipes: 
            1) without ingredients, hense with a price = 0
            2) with total price = 2.00 (1 ingredient)
            3) with total price = 5.00 (2 same ingredients by 2.50)
        """
        three_recipes = [
            self.recipe,
            RecipeFactory(),
            RecipeFactory()
        ]
        for i in range(1,3):
            RecipeIngredientFactory(recipe=three_recipes[i], quantity=i, ingredient__price=self.prices[i]) 
            self.total_prices[i] = three_recipes[i].calculated_total_price
        return three_recipes


    def test_setting_recipe_price(self):
        """Tests, if price is setting correctly (and stays decimal).
        Recipe's price should be set equal to decimal of 2.00
        """
        recipe_price = self.prices[1] # 2.00
        RecipeIngredientFactory(recipe=self.recipe, quantity=1, ingredient__price=recipe_price)

        self.assertEqual(recipe_price, self.recipe.calculated_total_price)
    
    
    # def test_recipe_filter_by_price_returns_all_if_price_not_set(self):
    #     """Tests Recipe.filter_by_price() behavior, when price range is not set.
    #     Recipe.filter_by_price() should return all 3 objects
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price()

    #     self.assertEqual(queryset.count(), len(self.three_recipes))


    # def test_recipe_filter_by_price_if_min_price_set_to_2(self):
    #     """Tests Recipe.filter_by_price() behavior, when only minimal price is set and is in the range, but not equal to one of the prices.
    #     Recipe.filter_by_price() should return 1 object with a price '5.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=Decimal('3.00'))

    #     self.assertEqual(1, queryset.count())
    #     self.assertEqual(queryset[0].price, self.three_recipes[2].price)


    # def test_recipe_filter_by_price_if_min_price_set_to_0(self):
    #     """Tests Recipe.filter_by_price() behavior, when only minimal price is set and is equal to 0.
    #     Recipe.filter_by_price() should return all 3 objects
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=self.total_prices[0]) # 0.00

    #     self.assertEqual(queryset.count(), len(self.three_recipes))


    # def test_recipe_filter_by_price_if_min_price_set_to_1(self):
    #     """Tests Recipe.filter_by_price() behavior, when only minimal price is set and is lt minimal price in range (except 0).
    #     Recipe.filter_by_price() should return 2 objects with prices '2.00' and '5.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=self.total_prices[1]) # 2.00
    #     prices = {recipe.price for recipe in queryset}

    #     self.assertTrue(self.total_prices[2] in prices)
    #     self.assertTrue(self.total_prices[1] in prices)
    #     self.assertEqual(2, queryset.count())

    
    # def test_recipe_filter_by_price_if_min_price_set_to_10(self):
    #     """Tests Recipe.filter_by_price() behavior, when only minimal price is set and is gt maximal price in range.
    #     Recipe.filter_by_price() should return no objects'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=Decimal('10.0'))

    #     self.assertEqual(0, queryset.count())        


    # def test_recipe_filter_by_price_if_max_price_set_to_05(self):
    #     """Tests Recipe.filter_by_price() behavior, when only maximum price is set, is fractional and is lt minimal price in range (except 0).
    #     Recipe.filter_by_price() should return 1 object with a price '0.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(max_price=Decimal('0.5'))

    #     self.assertEqual(1, queryset.count())
    #     self.assertEqual(queryset[0].price, self.three_recipes[0].price)


    # def test_recipe_filter_by_price_if_max_price_set_to_1(self):
    #     """Tests Recipe.filter_by_price() behavior, when only maximum price is set, is not fractional and is lt minimal price in range (except 0).
    #     Recipe.filter_by_price() should return 1 object with a price '0.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(max_price=Decimal('1.0'))

    #     self.assertEqual(1, queryset.count())
    #     self.assertEqual(queryset[0].price, self.three_recipes[0].price)


    # def test_recipe_filter_by_price_if_max_price_set_to_0(self):
    #     """Tests Recipe.filter_by_price() behavior, when only maximum price is set and is equal to 0.
    #     Recipe.filter_by_price() should return 1 object with a price '0.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(max_price=Decimal('0'))

    #     self.assertEqual(1, queryset.count())
    #     self.assertEqual(queryset[0].price, self.three_recipes[0].price)


    # def test_recipe_filter_by_price_if_max_price_set_to_3(self):
    #     """Tests Recipe.filter_by_price() behavior, when only maximum price is set and is in the range of not-0-prices, but not equal to one of the prices.
    #     Recipe.filter_by_price() should return 2 object with a price '0.00 and '2.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(max_price=Decimal('3.00'))
    #     prices = {recipe.price for recipe in queryset}

    #     self.assertTrue(self.total_prices[0] in prices)
    #     self.assertTrue(self.total_prices[1] in prices)
    #     self.assertEqual(2, queryset.count())


    # def test_recipe_filter_by_price_if_max_price_set_to_2(self):
    #     """Tests Recipe.filter_by_price() behavior, when only maximum price is set and is equal to one of the prices (except 0).
    #     Recipe.filter_by_price() should return 2 object with a price '0.00 and '2.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(max_price=self.total_prices[1]) # 2.00
    #     prices = {recipe.price for recipe in queryset}

    #     self.assertTrue(self.total_prices[0] in prices)
    #     self.assertTrue(self.total_prices[1] in prices)
    #     self.assertEqual(2, queryset.count())


    # def test_recipe_filter_by_price_if_max_price_set_gt_max_price(self):
    #     """Tests Recipe.filter_by_price() behavior, when  only maximum price is set and is out of range (gt).
    #     Recipe.filter_by_price() should return 3 object with prices '0.00', '2.00' and '5.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(max_price=Decimal('100')) 
    #     prices = {recipe.price for recipe in queryset}

    #     self.assertTrue(self.total_prices[0] in prices)
    #     self.assertTrue(self.total_prices[1] in prices)
    #     self.assertTrue(self.total_prices[2] in prices)
    #     self.assertEqual(3, queryset.count())


    # def test_recipe_filter_by_price_if_min_price_1_max_price_set_to_3(self):
    #     """Tests Recipe.filter_by_price() behavior, when both prices are set (but not to 0), are in range, but not equal to any particular price.
    #     Recipe.filter_by_price() should return 1 object with a price '2.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=Decimal('1.00'), max_price=Decimal('3.00'))

    #     self.assertEqual(1, queryset.count())
    #     self.assertEqual(queryset[0].price, self.three_recipes[1].price)


    # def test_recipe_filter_by_price_if_min_price_2_max_price_set_to_5(self):
    #     """Tests Recipe.filter_by_price() behavior, when both prices are set (but not to 0) and are equal to particular prices from the set.
    #     Recipe.filter_by_price() should return 2 object with a price '2.00' and '5.00'
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=self.total_prices[1], max_price=self.total_prices[2])
    #     prices = {recipe.price for recipe in queryset}

    #     self.assertTrue(self.total_prices[1] in prices)
    #     self.assertTrue(self.total_prices[2] in prices)        
    #     self.assertEqual(2, queryset.count())


    # def test_recipe_filter_by_price_if_min_price_10_max_price_set_to_20(self):
    #     """Tests Recipe.filter_by_price() behavior, when both prices are set and are out of range (gt).
    #     Recipe.filter_by_price() should return no objects.
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=Decimal('10.00'), max_price=Decimal('20.00'))
      
    #     self.assertEqual(0, queryset.count())


    # def test_recipe_filter_by_price_if_min_price_2_max_price_set_to_2(self):
    #     """Tests Recipe.filter_by_price() behavior, when both prices are set to one particular price from the set.
    #     Recipe.filter_by_price() should return 1 object with price of 2.00
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=self.three_recipes[1].price, max_price=self.three_recipes[1].price) # 2.00

    #     self.assertEqual(1, queryset.count())
    #     self.assertEqual(queryset[0].price, self.three_recipes[1].price)


    # def test_recipe_filter_by_price_if_min_price_3_max_price_set_to_2(self):
    #     """Tests Recipe.filter_by_price() behavior, when both prices are set, but the maximal one is less than the minimal one.
    #     Recipe.filter_by_price() should return no objects
    #     """
    #     self.three_recipes = self.setUp_three_recipes()
    #     queryset = Recipe.filter_by_price(min_price=Decimal('4.00'), max_price=Decimal('1.00'))

    #     self.assertEqual(0, queryset.count())
