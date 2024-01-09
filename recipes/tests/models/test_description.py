from django.test import TestCase
from django.core.exceptions import ValidationError
from recipes.models import Description

class DescriptionModelTestCase(TestCase):

    def setUp(self):
        self.description_data = {
            "name_en": "Test Description",
            "name_lv": "Testu apraksts",
            "name_ru": "Тестовое описание"
        }

    def assertDescriptionAttributes(self, description, expected_en, expected_lv, expected_ru):
        self.assertEqual(description.name_en, expected_en)
        self.assertEqual(description.name_lv, expected_lv)
        self.assertEqual(description.name_ru, expected_ru)

    def test_create_description(self):
        description = Description.objects.create(**self.description_data)
        self.assertEqual(Description.objects.count(), 1)
        self.assertDescriptionAttributes(description, "Test Description", "Testu apraksts", "Тестовое описание")

    def test_name_en_max_length(self):
        description = Description(name_en="a" * 5000)
        with self.assertRaises(ValidationError):
            description.full_clean()

    def test_name_lv_max_length(self):
        description = Description(name_en=self.description_data["name_en"], name_lv="b" * 5000)
        with self.assertRaises(ValidationError):
            description.full_clean()

    def test_name_ru_max_length(self):
        description = Description(name_en=self.description_data["name_en"], name_ru="c" * 5000)
        with self.assertRaises(ValidationError):
            description.full_clean()

    def test_str_representation(self):
        description = Description.objects.create(**self.description_data)
        self.assertEqual(str(description), self.description_data["name_en"])

    def test_null_and_blank_fields(self):
        description = Description.objects.create(name_en="Test Description", name_lv="", name_ru=None)
        self.assertEqual(description.name_lv, "")
        self.assertIsNone(description.name_ru)

    def test_update_and_save(self):
        description = Description.objects.create(**self.description_data)
        description.name_en = "Updated Description"
        description.name_lv = "Atjaunināts apraksts"
        description.name_ru = "Обновленное описание"
        description.save()
        self.assertEqual(Description.objects.count(), 1)
        self.assertDescriptionAttributes(description, "Updated Description", "Atjaunināts apraksts", "Обновленное описание")
