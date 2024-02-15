from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
import os 

from recipes import models

def manage_thumbnails(instance: 'models.RecipeImage') -> None:
    """
    Manage thumbnails for the given instance.

    Args:
        instance (RecipeImage): The instance for which thumbnails need to be managed.

    Returns:
        None
    """
    try:
        # Check if the thumbnail has not been generated yet
        if instance.image and instance.image.file and not instance.thumbnail:
            thumbnail = generate_thumbnail(instance)

            save_thumbnail(instance, thumbnail)
    except Exception as e:
        print(f"Error in manage_thumbnails: {e}")

def generate_thumbnail(instance: 'models.RecipeImage') -> Image.Image:
    """
    Generate a thumbnail for the given RecipeImage instance.

    Args:
        instance (RecipeImage): The RecipeImage instance.

    Returns:
        Image.Image: The generated thumbnail image.
    """
    try:
        # Open the original image using the storage backend
        with default_storage.open(instance.image.name) as img_file:
            img = Image.open(img_file)

        # Create a thumbnail using ImageOps
        thumbnail_size = (100, 100)
        thumbnail = ImageOps.fit(img, thumbnail_size)

        return thumbnail
    except Exception as e:
        print(f"Error in generate_thumbnail: {e}")
        return None

def save_thumbnail(instance: 'models.RecipeImage', thumbnail: Image.Image) -> None:
    """
    Save the thumbnail for the RecipeImage instance.

    Args:
        instance (RecipeImage): The RecipeImage instance.
        thumbnail (Image.Image): The thumbnail image to be saved.

    Returns:
        None
    """
    try:
        thumb_io = BytesIO()

        # Use the mode of the thumbnail to determine the format
        thumbnail_format = 'JPEG' if thumbnail.mode == 'RGB' else 'PNG'

        # Save the thumbnail with the determined format
        thumbnail.save(thumb_io, format=thumbnail_format)

        thumbnail_path = f"thumb_{os.path.basename(instance.image.name)}"
        instance.thumbnail.save(
            thumbnail_path,
            InMemoryUploadedFile(
                thumb_io,
                None,
                thumbnail_path,
                f'image/{thumbnail_format.lower()}',
                thumb_io.tell,
                None
            )
        )
    except Exception as e:
        print(f"Error in save_thumbnail: {e}")
