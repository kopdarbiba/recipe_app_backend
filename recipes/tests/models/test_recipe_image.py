import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from recipes.models import Recipe, RecipeImage, Title
from recipes.utils.thumbnail_utils import manage_thumbnails, generate_thumbnail, save_thumbnail


class RecipeImageSaveTestCase(TestCase):

    def setUp(self):
        self.title1 = Title.objects.create(name_en="Recipe 1", name_ru="Recipe 1", name_lv="Recipe 1")
        self.recipe = Recipe.objects.create(title=self.title1, cooking_time=1, servings=2)

        # Use the actual image content
        image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x03$IDATx\x9c\xec}\t\x94\xe3\xde9\xcfy\xe6\xf9\xf4\xc7\x1c\x87\x84\xbd\x1f\xd3\xb9?\xc9\xfc\x03\x00\x00\xf1zZY\x00\x00\x00\x00IEND\xaeB`\x82'
        
            # Print the image content for debugging
        print("Image Content:", image_content)
        # Check if the content starts with the correct PNG signature
        assert image_content.startswith(b'\x89PNG\r\n\x1a\n'), "Invalid PNG signature"

        self.recipe_image = RecipeImage(recipe=self.recipe)
        self.recipe_image.image = SimpleUploadedFile("test_image.png", image_content, content_type="image/png")

        # Ensure that the file extension is correct
        assert self.recipe_image.image.name.endswith('.png'), "Invalid file extension"


    def test_manage_thumbnails(self) -> None:
        """
        Test the manage_thumbnails function.
        """
        with patch('recipes.utils.thumbnail_utils.generate_thumbnail') as mock_generate_thumbnail, \
                patch('recipes.utils.thumbnail_utils.save_thumbnail') as mock_save_thumbnail:

            # Mock the generate_thumbnail function
            mock_thumbnail = MagicMock(spec=Image.Image)
            mock_generate_thumbnail.return_value = mock_thumbnail

            # Call the function
            manage_thumbnails(self.recipe_image)

            # Assertions
            mock_generate_thumbnail.assert_called_once_with(self.recipe_image.image)
            mock_save_thumbnail.assert_called_once_with(self.recipe_image, mock_thumbnail)

    def test_generate_thumbnail(self) -> None:
        """
        Test the generate_thumbnail function in different scenarios.
        """
            # Read the content from the ImageFieldFile before passing it to generate_thumbnail
        image_content = self.recipe_image.image.read()
        result = generate_thumbnail(image_content)

        # mock_image_open.assert_called_once_with('dummy_image.png')
        # mock_thumbnail.thumbnail.assert_called_once_with((100, 100))

        # Assertions
        self.assertEqual(result.mode, 'RGB')  # Assuming the mode is set correctly
        self.assertEqual(result.size, (100, 100))  # Set the expected size

        # Test case where 'convert' should not be called
        with patch('recipes.utils.thumbnail_utils.Image.open') as mock_image_open:
            mock_thumbnail = MagicMock(spec=Image.Image)
            mock_image_open.return_value = mock_thumbnail
            mock_thumbnail.mode = 'RGB'

            result = generate_thumbnail('dummy_image.jpg')

            mock_image_open.assert_called_once_with('dummy_image.jpg')
            mock_thumbnail.thumbnail.assert_called_once_with((100, 100))
            mock_thumbnail.convert.assert_not_called()
            self.assertEqual(result, mock_thumbnail)
