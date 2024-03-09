from rest_framework import viewsets
from recipes.models import Recipe, RecipeIngredient
from django.db.models import Prefetch
from recipes.serializers import RecipeSerializer
from .filters import RecipeFilter

class PriceFilterDemoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecipeFilter.by_total_price(Recipe.objects.all())
    serializer_class = RecipeSerializer

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
    
class RecipesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.select_related(
            'title', 
            'description', 
            'cuisine', 
            'occasion', 
            'meal'
            ).prefetch_related(
                'images', 
                'dietary_preferences',
                'instructions',
                'cooking_methods',
                'equipment',
                Prefetch("recipe_ingredients", queryset=RecipeIngredient.objects.select_related('ingredient', 'unit')),
                ).all()
    
    serializer_class = RecipeSerializer






# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

    # # GPT recomendation
    # @method_decorator(cache_page(5))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    # @method_decorator(cache_page(5))
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)