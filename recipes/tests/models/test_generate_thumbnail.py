# from django.test import TestCase
# from unittest.mock import patch, MagicMock
# from PIL import Image
# from io import BytesIO
# from django.core.files.uploadedfile import SimpleUploadedFile
# from recipes.utils.utilities import generate_thumbnail, save_thumbnail
# from recipes.models import generate_thumbnail_signal

# class ThumbnailGenerationTestCase(TestCase):
#     def setUp(self):
#         # Create a mock object with an 'image' field
#         self.mock_instance = MagicMock()

#         # Create a temporary image file for testing
#         image = Image.new('RGB', (100, 100))
#         self.mock_instance.image = MagicMock()
#         self.mock_instance.image.open.return_value = image

#         self.mock_instance.thumbnail = None

#     def test_generate_thumbnail(self):
#         # Call the function with the mock instance
#         result = generate_thumbnail(self.mock_instance)

#         # Assertions based on the result (modified img)
#         self.assertIsNotNone(result)  # Ensure a result is returned
#         self.assertIsNotNone(self.mock_instance.thumbnail)  # Ensure thumbnail attribute is set

#         # Additional assertions on the result (img properties)
#         self.assertEqual(result.size, (100, 100))  # Adjust as needed
#         # Add more assertions based on your requirements



#     # def test_save_thumbnail(self):
#     #     # Ensure that the mock instance has a thumbnail and image attribute
#     #     self.mock_instance.thumbnail = Image.new('RGB', (49, 49))
#     #     self.mock_instance.image = SimpleUploadedFile("test_image.jpg", b"dummy_content")

#     #     # Call the save_thumbnail function with the mock instance
#     #     save_thumbnail(self.mock_instance, self.mock_instance.thumbnail)

#     #     # Assertions based on the expected behavior of save_thumbnail
#     #     self.assertIsNotNone(self.mock_instance.thumbnail)  # Ensure thumbnail attribute is set

#     #     # Construct the expected thumbnail path
#     #     image_name = os.path.basename(self.mock_instance.image.name)
#     #     expected_thumbnail_path = f"thumb_{image_name}"

#     #     # Check if the thumbnail field is set with the correct path
#     #     self.assertEqual(self.mock_instance.thumbnail.name, expected_thumbnail_path)

#     #     # Check if the content of the thumbnail field matches the expected content
#     #     expected_thumbnail_content = b"dummy_content"  # Assuming thumbnail content is the same as image content
#     #     with self.mock_instance.thumbnail.open() as file:
#     #         actual_thumbnail_content = file.read()
#     #     self.assertEqual(actual_thumbnail_content, expected_thumbnail_content)

#     #     # Check if the format parameter passed to save_thumbnail is a string
#     #     self.assertIsInstance(self.mock_instance.thumbnail.format, str)

