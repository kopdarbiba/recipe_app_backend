from django.test import TestCase
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from recipes.models import Recipe, RecipeIngredient, Ingredient, Unit, Title

class RecipeIngredientTestCase(TestCase):

    def setUp(self):
        # Create Ingredients
        self.apple = Ingredient.objects.create(name_en="apple", name_ru="apple", name_lv="apple")
        self.pear = Ingredient.objects.create(name_en="pear", name_ru="pear", name_lv="pear")
        self.banana = Ingredient.objects.create(name_en="banana", name_ru="banana", name_lv="banana")

        # Create a Unit
        self.each_unit = Unit.objects.create(name_en="each",name_ru="each", name_lv="each")

        # Create Title
        self.title1 = Title.objects.create(name_en="Recipe 1", name_ru="Recipe 1", name_lv="Recipe 1")  
        self.title2 = Title.objects.create(name_en="Recipe 2", name_ru="Recipe 2", name_lv="Recipe 2")    

        # Create Recipes
        self.recipe1 = Recipe.objects.create(title=self.title1, cooking_time=1,servings=2)
        self.recipe2 = Recipe.objects.create(title=self.title2, cooking_time=3,servings=5)

        # Associate Ingredients with Recipes
        RecipeIngredient.objects.create(recipe=self.recipe1, ingredient=self.apple, quantity=3, unit=self.each_unit)
        RecipeIngredient.objects.create(recipe=self.recipe1, ingredient=self.pear, quantity=15.22, unit=self.each_unit)
        RecipeIngredient.objects.create(recipe=self.recipe2, ingredient=self.banana, quantity=2.22, unit=self.each_unit)
        RecipeIngredient.objects.create(recipe=self.recipe2, ingredient=self.banana, quantity=4.0, unit=self.each_unit)

        self.ingredients1 = RecipeIngredient.objects.filter(recipe=self.recipe1)
        self.ingredients2 = RecipeIngredient.objects.filter(recipe=self.recipe2)
        self.unique_ingredients1 = set(ing.ingredient for ing in self.ingredients1)
        self.unique_ingredients2 = set(ing.ingredient for ing in self.ingredients2)

    def test_ingredient_count(self):
        self.assertEqual(self.ingredients1.count(), 2)
        self.assertEqual(self.ingredients2.count(), 2)

    def test_ingredient_uniqueness(self):
        self.assertEqual(len(self.unique_ingredients1), 2)
        self.assertNotEqual(len(self.unique_ingredients2), 2)

    def test_valid_recipe(self):
        self.assertTrue(len(self.ingredients1) == 2 and len(set(ing.ingredient for ing in self.ingredients1)) == 2)
        self.assertFalse(len(self.ingredients2) == 2 and len(set(ing.ingredient for ing in self.ingredients2)) == 2)

    def test_quantity_more_than_two_decimal_places(self): # Quantity cannot be more than 2 decimal places due to DecimalField in the model, so this test will never fail unless model changes
        invalid_quantity = Decimal('3.111')
        ingredient = RecipeIngredient(
            recipe=self.recipe1, 
            ingredient=self.apple, 
            quantity=invalid_quantity, 
            unit=self.each_unit
        )

        with self.assertRaises(ValidationError):
            ingredient.full_clean()
       
    def test_quantities_are_two_decimal_places(self):
        for ingredient in RecipeIngredient.objects.all():
            self.assertEqual(ingredient.quantity, Decimal(ingredient.quantity).quantize(Decimal('0.00')),
                             f"Quantity for {ingredient.ingredient.name_en} was not saved correctly with two decimal places")
            
    def test_quantity_max_digits(self):
        for ingredient in RecipeIngredient.objects.all():
            total_digits = len(ingredient.quantity.normalize().as_tuple().digits)
            self.assertLessEqual(total_digits, 5, 
                                f"Quantity for {ingredient.ingredient.name_en} exceeds max_digits of 5")

    def test_save_and_update(self):
            ingredient = RecipeIngredient.objects.create(
                recipe=self.recipe1,
                ingredient=self.apple,
                quantity=Decimal('1.00'),
                unit=self.each_unit
            )
            ingredient.quantity = Decimal('2.00')
            ingredient.save()
            updated_ingredient = RecipeIngredient.objects.get(id=ingredient.id)
            self.assertEqual(updated_ingredient.quantity, Decimal('2.00'))

    def test_null_field_error(self):
        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(
                recipe=self.recipe1,
                ingredient=None,  # Set the foreign key to null
                quantity=Decimal('1.00'),
                unit=self.each_unit
            ) 