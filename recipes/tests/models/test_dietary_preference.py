from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import DietaryPreference

class DietaryPreferenceModelTestCase(TestCase):

    def setUp(self):
        self.dietary_preference_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertDietaryPreferenceAttributes(self, dietary_preference, expected_en, expected_lv, expected_ru):
        self.assertEqual(dietary_preference.name_en, expected_en)
        self.assertEqual(dietary_preference.name_lv, expected_lv)
        self.assertEqual(dietary_preference.name_ru, expected_ru)

    def test_create_dietary_preference(self):
        dietary_preference = DietaryPreference.objects.create(**self.dietary_preference_data)
        self.assertEqual(DietaryPreference.objects.count(), 1)
        self.assertDietaryPreferenceAttributes(dietary_preference, "a", "b", "c")

    def test_str_representation(self):
        meal = DietaryPreference.objects.create(**self.dietary_preference_data)
        self.assertEqual(str(meal), "a | b")

    def test_unique_constraint(self):
        DietaryPreference.objects.create(**self.dietary_preference_data)
        with self.assertRaises(IntegrityError):
            DietaryPreference.objects.create(name_en="a", name_lv="b", name_ru="c")
