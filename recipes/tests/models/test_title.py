from django.forms import ValidationError
from django.test import TestCase
from recipes.models import Title

class TitleModelTestCase(TestCase):

    def setUp(self):
        self.title_data = {
            "name_en": "Test Title", 
            "name_lv": "Testu virsraksts", 
            "name_ru": "Тестовое название"
        }

    def assertTitleAttributes(self, title, expected_en, expected_lv, expected_ru):
        self.assertEqual(title.name_en, expected_en)
        self.assertEqual(title.name_lv, expected_lv)
        self.assertEqual(title.name_ru, expected_ru)

    def test_create_title(self):
        title = Title.objects.create(**self.title_data)
        self.assertEqual(Title.objects.count(), 1)
        self.assertTitleAttributes(title, "Test Title", "Testu virsraksts", "Тестовое название")

    def test_str_representation(self):
        title = Title.objects.create(**self.title_data)
        self.assertEqual(str(title), self.title_data["name_en"])

    def test_null_and_blank_fields(self):
        title = Title.objects.create(name_en="Test Title", name_lv="", name_ru=None)
        self.assertEqual(title.name_lv, "")
        self.assertIsNone(title.name_ru)

    def test_max_length_validation(self):
        title = Title(name_en="a" * 256)
        with self.assertRaises(ValidationError):
            title.full_clean()

    def test_update_and_save(self):
        title = Title.objects.create(**self.title_data)
        title.name_en = "Updated Title"
        title.name_lv = "Atjaunināts virsraksts"
        title.name_ru = "Обновленное название"
        title.save()
        self.assertEqual(Title.objects.count(), 1)
        self.assertTitleAttributes(title, "Updated Title", "Atjaunināts virsraksts", "Обновленное название")
