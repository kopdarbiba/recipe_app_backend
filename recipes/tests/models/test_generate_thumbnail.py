from unittest import TestCase
from unittest.mock import MagicMock
from recipes.utils.utilities import generate_thumbnail


class ThumbnailGenerationTestCase(TestCase):
    def setUp(self):
        # Create a mock object with an 'image' field
        self.mock_instance = MagicMock()
        self.mock_instance.image = "dummy/path/"  # Set a dummy path

    def test_generate_thumbnail(self):
        # Call the function with the mock instance
        result = generate_thumbnail(self.mock_instance)

        print("Result:", result)
        print("Instance Thumbnail:", self.mock_instance.thumbnail)

        # Assertions or further testing based on the result
        self.assertIsNotNone(result)  # Ensure a result is returned
        self.assertIsNotNone(self.mock_instance.thumbnail)  # Ensure thumbnail attribute is set
        # Add more assertions based on your requirements


