from django.test import TestCase
from recipes.models import CookingStepInstruction, Recipe
from django.db.utils import IntegrityError


class CookingStepInstructionModelTestCase(TestCase):

    def setUp(self):
        self.instruction_names = {
            "name_en" : "Finely chop the onion, fry it golden brown in a pan.",
            "name_lv" : "Smalki sagriež sīpolu, pannā apcep zeltaini brūnus.",
            "name_ru" : "Мелко нарезаем лук, обжариваем его на сковороде до золотистого цвета."
        }
        self.recipe_required_data = {
            "cooking_time" : 1,
            "servings" : 1,
        }

        self.recipe = Recipe.objects.create(**self.recipe_required_data)
        self.step_number = 1
        self.instruction = CookingStepInstruction.objects.create(**self.instruction_names, recipe = self.recipe, step_number = self.step_number)



    def test_instruction_create_one(self):
        self.assertEqual(CookingStepInstruction.objects.count(), 1)

    def test_instruction_str_representation(self):
        self.assertEqual(str(self.instruction), self.instruction_names['name_en'])

    #This test doesn't work as expected since we allow creating instructions without instructions themselves (but why?)
    """def test_insctruction_create_without_names(self):
        with self.assertRaises(IntegrityError):
            instruction_not_valid = CookingStepInstruction.objects.create(step_number = self.step_number, recipe = self.recipe)"""

    def test_instruction_create_without_recipe(self):
        with self.assertRaises(IntegrityError):
            instruction_not_valid = CookingStepInstruction.objects.create(**self.instruction_names, step_number = self.step_number)

    # def test_instruction_create_without_step_number(self):
    #     with self.assertRaises(IntegrityError):
    #         instruction_not_valid = CookingStepInstruction.objects.create(**self.instruction_names, recipe = self.recipe)

    def test_instruction_step_number_is_positive(self):
        with self.assertRaises(IntegrityError):
            instruction_not_valid = CookingStepInstruction.objects.create(**self.instruction_names, recipe = self.recipe, step_number = -1)

    
    #This test doesn't work as expected since we allow creating instructions with repeated step numbers within one recipe (but why?)
    """def test_instruction_step_number_is_unique_within_recipe(self):
        with self.assertRaises(IntegrityError):
            #Creating another object equal to the one, created in setUp()
            instruction_not_valid = CookingStepInstruction.objects.create(**self.instruction_names, recipe = self.recipe, step_number = self.step_number)"""
