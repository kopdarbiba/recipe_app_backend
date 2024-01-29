import unittest
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError

from recipes.utils.utilities import delete_from_s3

class TestDeleteFromS3(unittest.TestCase):
    @patch('recipes.utils.utilities.get_s3_client')
    def test_delete_from_s3_success(self, mock_get_s3_client):
        # Mock the S3 client and its delete_object method for a successful deletion
        mock_s3_client = Mock()
        mock_s3_client.delete_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 204}}
        mock_get_s3_client.return_value = mock_s3_client

        # Call the function with a mock S3 key
        result = delete_from_s3('test_key')

        # Assert that the S3 client was called with the correct parameters
        mock_s3_client.delete_object.assert_called_once_with(Bucket='bildes-receptem', Key='test_key')

        # Assert that the function returned True for a successful deletion
        self.assertTrue(result)

    @patch('recipes.utils.utilities.get_s3_client')
    def test_delete_from_s3_failure(self, mock_get_s3_client):
        # Mock the S3 client and its delete_object method for a failure
        mock_s3_client = Mock()
        mock_s3_client.delete_object.side_effect = ClientError({'Error': {'Code': 'NoSuchKey'}}, 'operation_name')
        mock_get_s3_client.return_value = mock_s3_client

        # Call the function with a mock S3 key
        result = delete_from_s3('nonexistent_key')

        # Assert that the S3 client was called with the correct parameters
        mock_s3_client.delete_object.assert_called_once_with(Bucket='bildes-receptem', Key='nonexistent_key')

        # Assert that the function returned False for a failed deletion
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
