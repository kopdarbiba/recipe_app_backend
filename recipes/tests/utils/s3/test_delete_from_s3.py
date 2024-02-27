# ChatGPT action!!!



import unittest
from unittest.mock import patch
from django.conf import settings
from recipes.utils.s3_utils import delete_from_s3

class TestDeleteFromS3(unittest.TestCase):

    def setUp(self):
        # Mock the get_s3_client function
        self.get_s3_client_patch = patch('recipes.utils.s3_utils.get_s3_client')
        self.mock_get_s3_client = self.get_s3_client_patch.start()

        # Mocking the Django project settings
        settings.AWS_ACCESS_KEY_ID = 'your_access_key_id'
        settings.AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
        settings.AWS_S3_REGION_NAME = 'your_region'
        settings.AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'

    def tearDown(self):
        # Clean up resources after each test
        self.get_s3_client_patch.stop()

    def test_delete_from_s3_error(self):
        # Mock an error in delete_object
        expected_error_message = 'Simulating an error during object deletion'
        self.mock_get_s3_client.return_value.delete_object.side_effect = Exception(expected_error_message)

        # Call the function
        object_key = 'your_object_key'
        result = None
        with self.assertRaises(Exception, msg=expected_error_message):
            result = delete_from_s3(object_key)

        # Assertions
        self.assertIsNone(result)
        self.mock_get_s3_client.assert_called_once()

if __name__ == '__main__':
    unittest.main()
