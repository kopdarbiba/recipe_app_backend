# Import necessary modules
from django.test import TestCase
from recipes.tests.factory import RecipeFactory, TitleFactory


class RecipeTitleTestCase(TestCase):

    def setUp(self):
        # Create a Title using the TitleFactory
        title = TitleFactory(name_en='Test Recipe')
        
        # Create a Recipe using the RecipeFactory and associate it with the created Title
        recipe = RecipeFactory(title=title)

        # Store the created Title and Recipe for later use in the tests
        self.title = title
        self.recipe = recipe

    def test_recipe_title(self):
        # Assert that the title of the recipe matches the expected value
        self.assertEqual(self.recipe.title.name_en, 'Test Recipe')
