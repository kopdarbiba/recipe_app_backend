from rest_framework import viewsets, generics
from rest_framework import generics
from rest_framework.response import Response
from recipes.models import Recipe, RecipeIngredient
from recipes.serializers import RecipeSerializer, RecipePreviewSerializer
from .filters import RecipeFilter
from django.db.models import Prefetch

# View for returning recipes with minimal basic info: id, title, image(curently all images feched, but only one thumbnail img needed)
# Use in front page.
class RecipesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.select_related('title').prefetch_related('images').all()
    serializer_class = RecipePreviewSerializer

# TODO add filtering logic
class FindByIngredientsViewSet(viewsets.ReadOnlyModelViewSet):
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

# Example
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


# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

    # # GPT recomendation
    # @method_decorator(cache_page(5))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    # @method_decorator(cache_page(5))
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

class RecipeByCuisineView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        cuisine_name = self.kwargs.get('cuisine_name')
        if cuisine_name:
            return Recipe.objects.filter(cuisine__name_lv=cuisine_name)
        else:
            return Recipe.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)