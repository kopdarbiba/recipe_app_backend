import unittest
from unittest.mock import patch
from recipes.utils.utilities import get_s3_client

class TestGetS3Client(unittest.TestCase):
    @patch('recipes.utils.utilities.boto3.client')
    @patch('recipes.utils.utilities.settings.AWS_ACCESS_KEY_ID', 'test_access_key')
    @patch('recipes.utils.utilities.settings.AWS_SECRET_ACCESS_KEY', 'test_secret_key')
    @patch('recipes.utils.utilities.settings.AWS_S3_REGION_NAME', 'test_region')
    def test_get_s3_client(self, mock_boto_client):
        # Act: Call the function
        s3_client = get_s3_client()

        # Assert: Check if the S3 client has the correct configuration
        expected_params = {
            'aws_access_key_id': 'test_access_key',
            'aws_secret_access_key': 'test_secret_key',
            'region_name': 'test_region'
        }
        mock_boto_client.assert_called_once_with('s3', **expected_params)
        self.assertEqual(s3_client, mock_boto_client.return_value)

if __name__ == '__main__':
    unittest.main()
