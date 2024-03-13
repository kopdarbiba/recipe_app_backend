from rest_framework import viewsets
from recipes.models import Recipe, RecipeImage, RecipeIngredient
from django.db.models import Prefetch
from recipes.serializers import RecipeSerializer, RecipePreviewSerializer
from .filters import RecipeFilter

# View for returning recipes with minimal basic info: id, title, thumbnail
# Use in front page.
class FrontPageRecipesViewSet(viewsets.ReadOnlyModelViewSet):
    # Define a prefetch queryset for RecipeImage objects
    imgs = Prefetch('images', queryset=RecipeImage.objects.only('thumbnail', 'recipe_id').filter(is_main_image=True))
    
    # Define the base queryset with select_related and prefetch_related
    queryset = Recipe.objects.select_related('title').prefetch_related(imgs)
    
    def get_queryset(self):
        # Further optimize queryset by selecting only necessary title field based on language
        queryset = super().get_queryset()
        lang = self.request.query_params.get('lang', 'lv')
        queryset = queryset.only(f'title__name_{lang}')
        return queryset

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