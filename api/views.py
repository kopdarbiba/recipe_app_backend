from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from recipes.models import Recipe
from recipes.serializers import RecipeMinimalSerializer, RecipeSerializer, RecipeSearchPageSerializer
from recipes.utils.query_utils import get_prefetched_data
from recipes.filters import RecipeOrderingFilter, RecipeSearchFilter


class RecipeSearchAPIView(ListAPIView):
    """
    View to list all recipes with search ability.
    Example: http://localhost:8000/api/recipes/search/?lang=lv&ordering=total_price&q=šķēles
    """

    serializer_class = RecipeSearchPageSerializer
    filter_backends = [DjangoFilterBackend, RecipeSearchFilter, RecipeOrderingFilter]

    def get_queryset(self):
        queryset = get_prefetched_data(Recipe.objects.all(), main_img_only=True)

        return queryset

class RecipeList(ListAPIView):
    """
    View to list all recipes.
    Example: http://localhost:8000/api/recipes/?lang=en
    """
    serializer_class = RecipeMinimalSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        """
        Get method to retrieve all recipes.
        """
        queryset = get_prefetched_data(Recipe.objects.all(), main_img_only=True)
        return queryset

class RecipeDetails(RetrieveAPIView):
    """
    Retrieve details of a specific recipe.
    
    Example: http://localhost:8000/api/recipes/<id>/
    """

    serializer_class = RecipeSerializer

    def get_object(self):
        """
        Retrieve the recipe instance based on the id provided in the URL.
        """
        recipe_id = self.kwargs.get('pk')
        queryset = get_prefetched_data(Recipe.objects.all())
        recipe = get_object_or_404(queryset, pk=recipe_id)
        return recipe
