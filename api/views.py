from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipeList(APIView):
    """
    View to list all recipes.
    """

    def get(self, request):
        """
        Get method to retrieve all recipes.
        """
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
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
