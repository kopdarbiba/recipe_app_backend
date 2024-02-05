import os
from io import BytesIO
import logging
import boto3
from PIL import Image
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

def get_s3_client():
    """Get an S3 client with configured AWS credentials and region"""
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

def create_presigned_url(object_name, expiration):
    """Generate a presigned URL to share an S3 object
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Get an S3 client
    s3_client = get_s3_client()

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': object_name},
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        logging.error(e)
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None


def delete_from_s3(object_key):
    """Delete an object from S3
    :param object_key: string
    :return: True if successful, False otherwise
    """

    # Get an S3 client
    s3_client = get_s3_client()

    try:
        # Delete the object from S3
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=object_key)
        return True
    except ClientError as e:
        logging.error(e)
        return False
    

def generate_thumbnail(instance):
    if instance.image and not instance.thumbnail:
        # Open the original image using Pillow
        img = Image.open(instance.image)

        # Create a thumbnail
        thumbnail_size = (100, 100)  # Adjust the size as needed
        img.thumbnail(thumbnail_size)

        # Convert the image to RGB mode if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Save the thumbnail to the instance
        instance.thumbnail = 'img'
        instance.save()  # Save the instance to persist the thumbnail

        return img  # Return the thumbnail

    return None  # Return None if the conditions are not met


def save_thumbnail(instance, thumbnail):
    # Create an in-memory file
    thumb_io = BytesIO()
    thumbnail.save(thumb_io, format='JPEG')

    # Save the thumbnail to the thumbnail field
    image_name = os.path.basename(instance.image.name)
    thumbnail_path = f"thumb_{image_name}"
    instance.thumbnail.save(
        thumbnail_path,
        InMemoryUploadedFile(
            thumb_io,
            None,
            thumbnail_path,
            'image/jpeg',
            thumb_io.tell,
            None
        )
    )

