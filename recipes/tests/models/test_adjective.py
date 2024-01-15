from django.db.utils import IntegrityError
from django.test import TestCase
from recipes.models import Adjective

class AdjectiveModelTestCase(TestCase):

    def setUp(self):
        self.adjective_data = {
            "name_en": "a",
            "name_lv": "b",
            "name_ru": "c"
        }

    def assertAdjectiveAttributes(self, adjective, expected_en, expected_lv, expected_ru):
        self.assertEqual(adjective.name_en, expected_en)
        self.assertEqual(adjective.name_lv, expected_lv)
        self.assertEqual(adjective.name_ru, expected_ru)

    def test_create_adjective(self):
        adjective = Adjective.objects.create(**self.adjective_data)
        self.assertEqual(Adjective.objects.count(), 1)
        self.assertAdjectiveAttributes(adjective, "a", "b", "c")

    def test_str_representation(self):
        adjective = Adjective.objects.create(**self.adjective_data)
        self.assertEqual(str(adjective), "a | b")

    def test_unique_constraint(self):
        Adjective.objects.create(**self.adjective_data)
        with self.assertRaises(IntegrityError):
            Adjective.objects.create(name_en="a", name_lv="b", name_ru="c")
