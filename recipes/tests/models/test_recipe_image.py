# ChatGPT action!!!


from django.test import TestCase
from unittest.mock import patch, call
from recipes.models import Recipe, RecipeImage, Title, create_presigned_url

class RecipeImageTestCase(TestCase):
    def setUp(self):
        self.title1 = Title.objects.create(name_en="Recipe 1", name_ru="Recipe 1", name_lv="Recipe 1")  
        self.recipe = Recipe.objects.create(title=self.title1, cooking_time=1, servings=2)

        # Create a RecipeImage instance associated with the created Recipe
        self.instance = RecipeImage.objects.create(
            recipe=self.recipe,
            image='path/to/image.jpg',
            thumbnail='path/to/thumbnail.jpg'
        )

    @patch('recipes.models.create_presigned_url')
    def test_generate_presigned_url_for_image(self, mock_create_presigned_url):
        # Arrange
        expiration_time = 3600

        # Set up the mock's return value
        mock_create_presigned_url.return_value = 'mocked_presigned_url'

        # Act
        result = self.instance.generate_presigned_url_for_image(expiration_time)

        # Assert
        mock_create_presigned_url.assert_called_once_with(
            'path/to/image.jpg',
            expiration_time
        )

        # Check if the result matches the mocked value
        self.assertEqual(result, 'mocked_presigned_url')

    @patch('recipes.models.create_presigned_url')
    def test_generate_presigned_url_for_thumbnail(self, mock_create_presigned_url):
        # Arrange
        expiration_time = 3600

        # Set up the mock's return value
        mock_create_presigned_url.return_value = 'mocked_presigned_url'

        # Act
        result = self.instance.generate_presigned_url_for_thumbnail(expiration_time)

        # Assert
        mock_create_presigned_url.assert_called_once_with(
            'path/to/thumbnail.jpg',
            expiration_time
        )

        # Check if the result matches the mocked value
        self.assertEqual(result, 'mocked_presigned_url')

    @patch('recipes.models.delete_from_s3')
    def test_delete_method(self, mock_delete_from_s3):
        # Act
        self.instance.delete()

        # Assert
        expected_calls = [
            call('path/to/image.jpg'),
            call('path/to/thumbnail.jpg'),
        ]

        mock_delete_from_s3.assert_has_calls(expected_calls, any_order=True)

        # Check if the parent class's delete method was called
        self.assertIsNone(self.instance.pk)
