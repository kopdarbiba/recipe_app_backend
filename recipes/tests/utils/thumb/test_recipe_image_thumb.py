import unittest
from unittest.mock import patch, MagicMock, call
from io import BytesIO
from PIL import Image
from recipes.utils.thumbnail_utils import generate_thumbnail, save_thumbnail, image_to_bytes
from recipes import models

class TestThumbnailFunctions(unittest.TestCase):

    @patch('recipes.utils.thumbnail_utils.generate_thumbnail')
    @patch('recipes.utils.thumbnail_utils.image_to_bytes')
    @patch('recipes.utils.thumbnail_utils.save_thumbnail')
    @patch('django.core.files.storage.default_storage.open')
    def test_manage_thumbnails(self, mock_open, mock_save_thumbnail, mock_image_to_bytes, mock_generate_thumbnail):
        mock_instance = MagicMock()
        mock_instance.image.name = "test_image.png"

        # Mock instance.thumbnail with a None value
        mock_instance.thumbnail = None

        # Set the known value for original_image_in_bytes and thumbnail_image_object
        original_image_in_bytes = b'fake_image_content'
        thumbnail_image_bytes = b'fake_thumbnail_content'

        # Set image object for thumbnail_image_object
        thumbnail_img_obj = Image.new('RGB', (100, 100))

        # Set up the mock_open side effect to return the known value
        mock_open.return_value.__enter__.return_value.read.return_value = original_image_in_bytes

        # Set up the side effect for generate_thumbnail to return a known value
        mock_generate_thumbnail.side_effect = lambda x: thumbnail_img_obj

        # Set up the return value for image_to_bytes
        mock_image_to_bytes.return_value = thumbnail_image_bytes


        # Call the function with the known value
        models.manage_thumbnails(mock_instance)

        # Assert that generate_thumbnail was called with the expected argument
        mock_generate_thumbnail.assert_called_once_with(original_image_in_bytes)

        # Assert that image_to_bytes was called with the expected argument
        mock_image_to_bytes.assert_called_once_with(thumbnail_img_obj)

        # Assert that save_thumbnail was called with the correct arguments
        mock_save_thumbnail.assert_called_once_with(mock_instance, thumbnail_image_bytes)

    def test_generate_thumbnail_success(self):
        # Create a dummy original image
        original_image = Image.new('RGB', (200, 200), color='blue')
        original_image_io = BytesIO()
        original_image.save(original_image_io, format='PNG')
        original_image_bytes = original_image_io.getvalue()

        # Call the generate_thumbnail function
        thumbnail_result = generate_thumbnail(original_image_bytes)

        # Check if the result is an instance of PIL Image
        self.assertIsInstance(thumbnail_result, Image.Image)

        # Check if the size of the generated thumbnail is correct
        self.assertEqual(thumbnail_result.size, (99, 99))

    def test_image_to_bytes_with_valid_image(self):
        # Create a dummy image
        dummy_image = Image.new('RGB', (100, 100), color='red')

        # Convert the image to bytes
        result_bytes = image_to_bytes(dummy_image)

        # Check if the result is bytes
        self.assertIsInstance(result_bytes, bytes)

        # Check if the length of the result is not zero
        self.assertNotEqual(len(result_bytes), 0)

    def test_image_to_bytes_with_none_image(self):
        # Pass None as input
        result_bytes = image_to_bytes(None)

        # Check if the result is None
        self.assertIsNone(result_bytes)

    def test_save_thumbnail_success(self):
        # Mock the RecipeImage instance
        instance_mock = MagicMock()
        instance_mock.image.name = "example_image.png"

        # Mock the thumbnail data
        thumbnail_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...'

        # Call the save_thumbnail function
        save_thumbnail(instance_mock, thumbnail_data)

        # Check if the save method of the instance is called
        instance_mock.save.assert_called_once()


