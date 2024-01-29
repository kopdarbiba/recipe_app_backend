# from django.test import TestCase
# from moto import mock_s3
# from recipes.models import RecipeImage, Recipe, Title
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.contrib.auth.models import User

# @mock_s3
# class RecipeImageModelTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()

#         # Start the moto mock
#         cls.mock_s3 = mock_s3()
#         cls.mock_s3.start()

#     @classmethod
#     def tearDownClass(cls):
#         # Stop the moto mock
#         cls.mock_s3.stop()
#         super().tearDownClass()

#     def setUp(self):
#         self.title1 = Title.objects.create(name_en="Recipe 1", name_ru="Recipe 1", name_lv="Recipe 1")  
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.recipe = Recipe.objects.create(title=self.title1, cooking_time=1, servings=2)

#         # Load the test image from the fixtures directory
#         image_path = 'recipes/tests/fixtures/test_image.png'
#         with open(image_path, 'rb') as file:
#             self.image = SimpleUploadedFile("test_image.png", file.read(), content_type="image/png")

#         self.recipe_image = RecipeImage.objects.create(recipe=self.recipe, image=self.image)

#     def test_test(self):
#         self.assertTrue(True)
