from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import Meal

class MealModelTestCase(TestCase):

    def setUp(self):
        self.meal_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertMealAttributes(self, meal, expected_en, expected_lv, expected_ru):
        self.assertEqual(meal.name_en, expected_en)
        self.assertEqual(meal.name_lv, expected_lv)
        self.assertEqual(meal.name_ru, expected_ru)

    def test_create_meal(self):
        meal = Meal.objects.create(**self.meal_data)
        self.assertEqual(Meal.objects.count(), 1)
        self.assertMealAttributes(meal, "a", "b", "c")

    def test_str_representation(self):
        meal = Meal.objects.create(**self.meal_data)
        self.assertEqual(str(meal), "a | b")

    def test_unique_constraint(self):
        Meal.objects.create(**self.meal_data)
        with self.assertRaises(IntegrityError):
            Meal.objects.create(name_en="a", name_lv="b", name_ru="c")
