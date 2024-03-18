from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from django.db.models import Prefetch

from recipes.models import Recipe, RecipeIngredient
from recipes.serializers import RecipeSerializer


class RecipeList(APIView):
    """
    View to list all recipes.
    Example: http://localhost:8000/api/recipes/?lang=en
    """

    def get(self, request):
        """
        Get method to retrieve all recipes.
        """
        # Set default language to 'lv' if not provided
        lang = request.query_params.get('lang', 'lv')
        lang_field_name = f'name_{lang}'

        # Retrieve recipes with related data
        recipes = Recipe.objects.select_related(
            'title', 
            'description',
            'cuisine',
            'occasion',
            'meal'
        ).prefetch_related(
            'images', 
            'instructions', 
            Prefetch(
                "recipe_ingredients", 
                queryset=RecipeIngredient.objects.select_related(
                    'ingredient', 
                    'unit',
                    'ingredient__allergen', 
                    'ingredient__category'
                )
            ),
            'equipment',
            'cooking_methods'
        )

        # Serialize data with the specified language context
        serializer = RecipeSerializer(recipes, many=True, context={'lang_field_name': lang_field_name})

        return Response(serializer.data)

class RecipeDetails(APIView):
    """
    View to retrieve a single recipe.
    """

    def get_object(self, pk):
        """
        Helper method to get a recipe object by its primary key.
        """
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        """
        Get method to retrieve a single recipe by its primary key.
        """
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)
