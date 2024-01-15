from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import Occasion

class OccasionModelTestCase(TestCase):

    def setUp(self):
        self.occasion_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertOccasionAttributes(self, occasion, expected_en, expected_lv, expected_ru):
        self.assertEqual(occasion.name_en, expected_en)
        self.assertEqual(occasion.name_lv, expected_lv)
        self.assertEqual(occasion.name_ru, expected_ru)

    def test_create_occasion(self):
        occasion = Occasion.objects.create(**self.occasion_data)
        self.assertEqual(Occasion.objects.count(), 1)
        self.assertOccasionAttributes(occasion, "a", "b", "c")

    def test_str_representation(self):
        occasion = Occasion.objects.create(**self.occasion_data)
        self.assertEqual(str(occasion), "a | b")

    def test_unique_constraint(self):
        Occasion.objects.create(**self.occasion_data)
        with self.assertRaises(IntegrityError):
            Occasion.objects.create(name_en="a", name_lv="b", name_ru="c")
