from django.test import TestCase
from unittest.mock import patch, call
from recipes.models import RecipeImage, delete_from_s3

class RecipeImageTestCase(TestCase):
    @patch('recipes.models.delete_from_s3')
    def test_delete_method(self, mock_delete_from_s3):
        # Arrange
        # Create a RecipeImage instance without associating it with a Recipe
        instance = RecipeImage.objects.create(recipe_id=1, image='path/to/image.jpg', thumbnail='path/to/thumbnail.jpg')  

        # Act
        instance.delete()

        # Assert
        expected_calls = [
            call('path/to/image.jpg'),
            call('path/to/thumbnail.jpg'),
        ]

        mock_delete_from_s3.assert_has_calls(expected_calls, any_order=True)

        # Check if the parent class's delete method was called
        self.assertIsNone(instance.pk)

