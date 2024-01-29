# Warning!!! This test is chatGPT generated!!!

import unittest
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from django.conf import settings

from recipes.utils.utilities import create_presigned_url

class TestCreatePresignedUrl(unittest.TestCase):
    @patch('recipes.utils.utilities.get_s3_client')
    def test_create_presigned_url_success(self, mock_get_s3_client):
        # Mock the S3 client and its generate_presigned_url method for a successful URL generation
        mock_s3_client = Mock()
        mock_s3_client.generate_presigned_url.return_value = 'https://example.com/s3/signed-url'
        mock_get_s3_client.return_value = mock_s3_client

        # Call the function with a mock S3 key
        result = create_presigned_url('test_key', expiration=3600)

        # Assert that the S3 client was called with the correct parameters
        expected_params = {
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': 'test_key',
        }
        mock_s3_client.generate_presigned_url.assert_called_once_with('get_object', Params=expected_params, ExpiresIn=3600)

        # Assert that the function returned the expected signed URL
        self.assertEqual(result, 'https://example.com/s3/signed-url')

    @patch('recipes.utils.utilities.get_s3_client')
    def test_create_presigned_url_failure(self, mock_get_s3_client):
        # Mock the S3 client and its generate_presigned_url method for a failure
        mock_s3_client = Mock()
        mock_s3_client.generate_presigned_url.side_effect = ClientError({'Error': {'Code': 'AccessDenied'}}, 'operation_name')
        mock_get_s3_client.return_value = mock_s3_client

        # Call the function with a mock S3 key
        result = create_presigned_url('nonexistent_key', expiration=3600)

        # Assert that the S3 client was called with the correct parameters
        expected_params = {
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': 'nonexistent_key',
        }
        mock_s3_client.generate_presigned_url.assert_called_once_with('get_object', Params=expected_params, ExpiresIn=3600)

        # Assert that the function returned None for a failed URL generation
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
