from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import Cuisine

class CuisineModelTestCase(TestCase):

    def setUp(self):
        self.cuisine_data = {
            "name_en": "Italian",
            "name_lv": "Itāliešu",
            "name_ru": "Итальянская"
        }

    def assertCuisineAttributes(self, cuisine, expected_en, expected_lv, expected_ru):
        self.assertEqual(cuisine.name_en, expected_en)
        self.assertEqual(cuisine.name_lv, expected_lv)
        self.assertEqual(cuisine.name_ru, expected_ru)

    def test_create_cuisine(self):
        cuisine = Cuisine.objects.create(**self.cuisine_data)
        self.assertEqual(Cuisine.objects.count(), 1)
        self.assertCuisineAttributes(cuisine, "Italian", "Itāliešu", "Итальянская")

    def test_str_representation(self):
        cuisine = Cuisine.objects.create(**self.cuisine_data)
        self.assertEqual(str(cuisine), "Italian | Itāliešu")

    def test_unique_constraint(self):
        Cuisine.objects.create(**self.cuisine_data)  # Create the first cuisine
        # Try to create a cuisine with the same name_en and name_lv (which should be unique)
        with self.assertRaises(IntegrityError):
            Cuisine.objects.create(name_en="Italian", name_lv="Itāliešu", name_ru="Another Cuisine")
