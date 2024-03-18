from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from recipes.models import Recipe, RecipeIngredient
from recipes.serializers import RecipeSerializer


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
