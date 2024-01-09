
# from django.test import TestCase
# from decimal import Decimal
# from recipes.models import Ingredient



# class IngredientModelTestCase(TestCase):
#     fixtures = ['recipes/fixtures/recipes_data.json']

#     def setUp(self) -> None:
#         None


#     def test_ingredients_price(self):
#         ingredient = Ingredient.objects.get(name_en='pork')

#         # Set the precision to two decimal places for comparison
#         expected_price = Decimal('72.90').quantize(Decimal('0.00'))

#         self.assertEqual(ingredient.price, expected_price)
