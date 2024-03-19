from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from decimal import Decimal

from recipes.models import Recipe, RecipeIngredient
from recipes.serializers import RecipeMinimalSerializer, RecipeSerializer


class RecipeList(ListAPIView):
    """
    View to list all recipes.
    Example: http://localhost:8000/api/recipes/?lang=en
    """

    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination


    def get_queryset(self):
        """
        Get method to retrieve all recipes.
        """
        # Retrieve recipes with related data
        prefetched_recipe_ingredients = Prefetch("recipe_ingredients", queryset=RecipeIngredient.objects.select_related(
                    'ingredient', 
                    'unit',
                    'ingredient__allergen', 
                    'ingredient__category'
                )
            ) 
        queryset = Recipe.objects.select_related(
            'title', 
            'description',
            'cuisine',
            'occasion',
            'meal'
        ).prefetch_related(
            'images', 
            'instructions', 
            'equipment',
            'cooking_methods',
            prefetched_recipe_ingredients,
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Set default language to 'lv' if not provided
        lang = self.request.query_params.get('lang', 'lv')
        lang_field_name = f'name_{lang}'

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'lang_field_name': lang_field_name})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'lang_field_name': lang_field_name})
        return Response(serializer.data)

class RecipeFilterList(ListAPIView):
    """
    View to list all recipes.
    Example: http://localhost:8000/api/recipes/filter/?lang=lv&min_price=999&max_price=8989
    """

    # queryset = Recipe.receptes_mngr.filter_by_title('kotletes')

    serializer_class = RecipeMinimalSerializer
    pagination_class = PageNumberPagination
    ordering_fields = ['total_price', 'title', 'cooking_time', 'servings']
    ordering = ['total_price']  # You can remove this line if you want to apply custom ordering

    def get_queryset(self):
        # Get the queryset from the manager
        qs_sorted_recipes = Recipe.receptes_mngr.sort_by_total_price()
        
        # Retrieve the min_price and max_price query parameters from the request
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        # Convert min_price and max_price to Decimal, with default values if not provided
        min_price_decimal = Decimal(min_price) if min_price else Decimal('0.00')
        max_price_decimal = Decimal(max_price) if max_price else None
        
        # Filter sorted recipes by price range
        queryset = Recipe.receptes_mngr.filter_by_price(qs_sorted_recipes, min_price=min_price_decimal, max_price=max_price_decimal)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Set default language to 'lv' if not provided
        lang = self.request.query_params.get('lang', 'lv')
        lang_field_name = f'name_{lang}'

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'lang_field_name': lang_field_name})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'lang_field_name': lang_field_name})
        return Response(serializer.data)
