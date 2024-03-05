from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from recipes.models import Recipe

from recipes.serializers import RecipeSerializer
from .filters import RecipeFilter

class PriceFilterDemoViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = RecipeFilter.by_total_price(Recipe.objects.all())

    filter_backends = [OrderingFilter]
    ordering_fields = ['total_price', 'title', 'cooking_time', 'servings']
    ordering = ['total_price']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Extract min_price and max_price from query parameters
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        # Apply price range filtering
        queryset = RecipeFilter.by_price_range(queryset, min_price, max_price)

        return queryset