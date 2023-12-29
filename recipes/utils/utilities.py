import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

def create_presigned_url(object_name, expiration):
    """Generate a presigned URL to share an S3 object
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Access AWS credentials from settings
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    aws_region_name = settings.AWS_S3_REGION_NAME
    aws_bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region_name
    )

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': aws_bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        logging.error(e)
        return None
