from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from recipes import models

def manage_thumbnails(instance: 'models.RecipeImage') -> None:
    """
    Manage thumbnails for the given instance.

    This function checks if a thumbnail has not been generated for the given instance. If not,
    it reads the original image, generates a thumbnail, and saves it.

    Args:
        instance (models.RecipeImage): The instance for which thumbnails need to be managed.

    Returns:
        None
    """
    try:
        if instance.image and instance.image.file and not instance.thumbnail:
            with default_storage.open(instance.image.name, 'rb') as f:
                original_image_in_bytes = f.read()

            thumb_img_obj = generate_thumbnail(original_image_in_bytes)
            if thumb_img_obj:
                thumb_img_bytes = image_to_bytes(thumb_img_obj)
                save_thumbnail(instance, thumb_img_bytes)

    except Exception as e:
        print(f"Error in manage_thumbnails: {e}")


def generate_thumbnail(original_image_in_bytes: bytes) -> Image.Image:
    """
    Generate thumbnail from the original image bytes.

    Args:
        original_image_in_bytes (bytes): The byte data of the original image.

    Returns:
        PIL.Image: The thumbnail image object.
    """
    try:
        with BytesIO(original_image_in_bytes) as img_io:
            thumbnail_img = Image.open(img_io)
            thumbnail_size = (99, 99)
            thumbnail_img.thumbnail(thumbnail_size)
            return thumbnail_img
    except OSError as processing_error:
        print(f"Error processing image: {processing_error}")
        return None


def image_to_bytes(image: Image.Image) -> bytes:
    """
    Convert a PIL Image object to bytes.

    Args:
        image (PIL.Image): The image object to convert.

    Returns:
        bytes: The byte data of the image.
    """
    if image is None:
        return None
    with BytesIO() as thumb_io:
        image.save(thumb_io, format='PNG')
        return thumb_io.getvalue()


def save_thumbnail(instance: 'models.RecipeImage', thumbnail_data: bytes) -> None:
    """
    Save the thumbnail image and update the model instance.

    This function saves the thumbnail image to the specified path and updates the
    model instance with the new thumbnail path.

    Args:
        instance (models.RecipeImage): The RecipeImage model instance.
        thumbnail_data (bytes): The byte data of the thumbnail image.

    Returns:
        None
    """
    try:
        thumbnail_path = f"thumb_{os.path.basename(instance.image.name)}"
        instance.thumbnail.save(
            thumbnail_path,
            ContentFile(thumbnail_data),
            save=False
        )
        instance.save()
    except Exception as e:
        print(f"Error in save_thumbnail: {e}")
