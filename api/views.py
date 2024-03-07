from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from recipes.models import Recipe
from django.db.models import Count

from recipes.serializers import RecipeSerializer
from .filters import RecipeFilter

class PriceFilterDemoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecipeFilter.by_total_price(Recipe.objects.all())
    serializer_class = RecipeSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ['total_price', 'title', 'cooking_time', 'servings']
    ordering = ['total_price']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Extract min_price, max_price, and ingredient_ids from query parameters
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        ingredient_ids = self.request.query_params.getlist('ingredient_ids')

        # Apply filters
        queryset = RecipeFilter.by_price_range(queryset, min_price, max_price)
        queryset = RecipeFilter.by_ingredients(queryset, ingredient_ids)
        
        return queryset