# # yourapp/tests/test_models.py
# from django.test import TestCase
# from django.core.files.uploadedfile import SimpleUploadedFile
# from recipes.models import Recipe, RecipeImage, Title
# from recipes.utils.utilities import delete_from_s3
# from recipes.models import delete_s3_images  # Import the signal handler

# class RecipeImageSignalTests(TestCase):
#     def setUp(self):
#         self.title1 = Title.objects.create(name_en="Recipe 1", name_ru="Recipe 1", name_lv="Recipe 1")  
#         self.recipe = Recipe.objects.create(title=self.title1, cooking_time=1, servings=2)

#         # Create a RecipeImage with both image and thumbnail
#         image = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
#         thumbnail = SimpleUploadedFile("thumbnail.jpg", b"file_content", content_type="image/jpeg")
#         self.recipe_image = RecipeImage.objects.create(recipe=self.recipe, image=image, thumbnail=thumbnail)

#     def test_delete_s3_images_signal(self):
#         # Call the signal handler directly
#         delete_s3_images(sender=RecipeImage, instance=self.recipe_image)

#         # Check if the S3 objects associated with the instance are deleted
#         s3_key_image = self.recipe_image.image.name
#         s3_key_thumbnail = self.recipe_image.thumbnail.name

#         self.assertIsNone(delete_from_s3(s3_key_image))  # Assuming delete_from_s3 returns None on success
#         self.assertIsNone(delete_from_s3(s3_key_thumbnail))
