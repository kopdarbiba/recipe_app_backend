from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Recipe
from recipes.serializers import RecipeMinimalSerializer, RecipeSerializer
from recipes.utils.query_utils import get_prefetched_data
from recipes.filters import RecipeOrderingFilter, RecipeSearchFilter


class RecipeSearchAPIView(ListAPIView):
    """
    View to list all recipes with search ability.
    Example: http://localhost:8000/api/recipes/search/?lang=lv&ordering=total_price&q=šķēles
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeMinimalSerializer
    filter_backends = [DjangoFilterBackend, RecipeSearchFilter, RecipeOrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = get_prefetched_data(queryset)
        return queryset

class RecipeList(ListAPIView):
    """
    View to list all recipes.
    Example: http://localhost:8000/api/recipes/?lang=en
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self, *args, **kwargs):
        """
        Get method to retrieve all recipes.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = get_prefetched_data(queryset)
        return queryset

