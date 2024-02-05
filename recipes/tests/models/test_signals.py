# from django.test import TestCase
# from django.db.models.signals import post_save
# from PIL import Image
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from recipes.models import Recipe, RecipeImage, Title, generate_thumbnail
# from unittest.mock import Mock

# class RecipeImageSignalsTest(TestCase):
#     def setUp(self):
#         self.title1 = Title.objects.create(name_en="Recipe 1", name_ru="Recipe 1", name_lv="Recipe 1")
#         self.recipe = Recipe.objects.create(title=self.title1, cooking_time=1, servings=2)

#         # Create a sample RecipeImage instance with image data and associate it with the Recipe
#         image_data = BytesIO()
#         image = Image.new('RGB', size=(200, 200), color='red')
#         image.save(image_data, format='JPEG')
#         image_data.seek(0)
#         self.image_file = InMemoryUploadedFile(
#             image_data,
#             None,
#             "test_image.jpg",
#             "image/jpeg",
#             image_data.tell,
#             None
#         )

#     def test_generate_thumbnail_signal(self):
#         # Create a mock object for generate_thumbnail
#         mock_generate_thumbnail = Mock()

#         # Connect the mock_generate_thumbnail function to the post_save signal
#         post_save.connect(mock_generate_thumbnail, sender=RecipeImage, dispatch_uid="test_signal")

#         # Create a dummy RecipeImage instance
#         recipe_image = RecipeImage.objects.create(recipe=self.recipe, image=self.image_file)

#         # Ensure that the mock_generate_thumbnail function was called once
#         mock_generate_thumbnail.assert_called_once_with(sender=RecipeImage, instance=recipe_image, created=True)

#         # Disconnect the mock_generate_thumbnail from the signal
#         post_save.disconnect(mock_generate_thumbnail, sender=RecipeImage, dispatch_uid="test_signal")
