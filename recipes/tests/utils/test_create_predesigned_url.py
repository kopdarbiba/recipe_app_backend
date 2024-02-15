# ChatGPT action!!!


import unittest
from unittest.mock import patch
from django.conf import settings
from recipes.utils.s3_utils import create_presigned_url
import logging

class TestCreatePresignedUrl(unittest.TestCase):

    def setUp(self):
        # Mock the get_s3_client function
        self.get_s3_client_patch = patch('recipes.utils.s3_utils.get_s3_client')
        self.mock_get_s3_client = self.get_s3_client_patch.start()

        # Mocking the Django project settings
        settings.AWS_ACCESS_KEY_ID = 'your_access_key_id'
        settings.AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
        settings.AWS_S3_REGION_NAME = 'your_region'
        settings.AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
        
        # Enable logging for unit-test
        logging.basicConfig(filename='test_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    def tearDown(self):
        # Clean up resources after each test
        self.get_s3_client_patch.stop()

    def test_create_presigned_url_success(self):
        # Mock the response from generate_presigned_url
        mock_presigned_url = 'https://your-presigned-url.com'
        self.mock_get_s3_client.return_value.generate_presigned_url.return_value = mock_presigned_url

        # Call the function
        object_name = 'your_object_key'
        expiration = 3600
        presigned_url = create_presigned_url(object_name, expiration)

        # Assertions
        self.assertEqual(presigned_url, mock_presigned_url)
        self.mock_get_s3_client.assert_called_once()

    def test_create_presigned_url_error(self):
        # Mock an error in generate_presigned_url
        self.mock_get_s3_client.return_value.generate_presigned_url.side_effect = Exception('Simulating an error during predesigned URL creation in unit-test')

        # Call the function
        object_name = 'your_object_key'
        expiration = 3600
        presigned_url = create_presigned_url(object_name, expiration)

        # Assertions
        self.assertIsNone(presigned_url)
        self.mock_get_s3_client.assert_called_once()
        

if __name__ == '__main__':
    unittest.main()