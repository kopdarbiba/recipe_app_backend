# ChatGPT action!!!


import unittest
from unittest.mock import patch
from django.conf import settings
from recipes.utils.s3_utils import get_s3_client


class TestGetS3Client(unittest.TestCase):

    def setUp(self):
        # Mock the boto3.client method for the entire test case
        self.boto3_client_patch = patch('recipes.utils.s3_utils.boto3.client')
        self.mock_boto3_client = self.boto3_client_patch.start()

        # Mocking the Django project settings
        settings.AWS_ACCESS_KEY_ID = 'your_access_key_id'
        settings.AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
        settings.AWS_S3_REGION_NAME = 'your_region'

    def tearDown(self):
        # Clean up resources after each test
        self.boto3_client_patch.stop()

    def test_get_s3_client(self):
        # Call the function
        s3_client = get_s3_client()

        # Assertions
        self.mock_boto3_client.assert_called_once_with(
            's3',
            aws_access_key_id='your_access_key_id',
            aws_secret_access_key='your_secret_access_key',
            region_name='your_region'
        )

        self.assertEqual(s3_client, self.mock_boto3_client.return_value)

if __name__ == '__main__':
    unittest.main()
