from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from decimal import Decimal

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer



class ComplexSearchView(ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        cuisine_name = self.request.GET.get('cuisine', '')
        meal_name = self.request.GET.get('meal', '')
        ingredient_names = self.request.GET.get('ingredients', '').split(',')
        dietary_preferences = self.request.GET.get('dietary_preferences', '').split(',')
        equipment_names = self.request.GET.get('equipment', '').split(',')
        cooking_methods = self.request.GET.get('cooking_methods', '').split(',')

        if ingredient_names or cuisine_name or meal_name or dietary_preferences or equipment_names or cooking_methods:
            queryset = Recipe.objects.all()

            if cuisine_name:
                queryset = queryset.filter(cuisine__name_en__icontains=cuisine_name)
            if meal_name:
                queryset = queryset.filter(meal__name_en__icontains=meal_name)

            for ingredient_name in ingredient_names:
                queryset = queryset.filter(recipe_ingredients__ingredient__name_en__icontains=ingredient_name)

            for preference in dietary_preferences:
                queryset = queryset.filter(dietary_preferences__name_en__icontains=preference)

            for equipment_name in equipment_names:
                queryset = queryset.filter(equipment__name_en__icontains=equipment_name)

            for cooking_method in cooking_methods:
                queryset = queryset.filter(cooking_methods__name_en__icontains=cooking_method)

            # Add other filters based on additional parameters

            return queryset.distinct()

        return Recipe.objects.none()

    
class RecipesByIngredientView(ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        ingredient_names = self.request.GET.get('ingredients', '').split(',')

        if ingredient_names:
            queryset = Recipe.objects.all()
            for ingredient_name in ingredient_names:
                # Use '__ingredient__name_eng__icontains' for case-insensitive search
                queryset = queryset.filter(recipe_ingredients__ingredient__name_en__icontains=ingredient_name)

            return queryset.distinct()

        return Recipe.objects.none()
    

class RecipesByPriceView(ListAPIView):
    """Working APIview endpoint example that return recipes, filtered by price (with pagination).
    Accepts optional GET params 'min' and 'max' for price.
    Works at http://localhost:8000/recipes/recipes-by-price/"""
    serializer_class = RecipeSerializer

    def get_queryset(self):
        try:
            min_price = Decimal(self.request.GET['min']) if 'min' in self.request.GET else Decimal('0.00')
            max_price = Decimal(self.request.GET['max']) if 'max' in self.request.GET else None 
        except:
            return Response({'Error': 'price should be numeric'})
        
        return Recipe.filter_by_price(min_price, max_price).distinct()


class RecipesViewSet(viewsets.ModelViewSet):
    """Working ViewSet endpoint example that returns all of the recipes (with pagination).
    Works at http://localhost:8000/recipes/recipes-set/"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class RecipesByPriceViewSet(viewsets.ViewSet):
    """Working ViewSet endpoint example (with pagination, but without pagination buttons (have no idea, why so)).
    Accepts optional GET params 'min' and 'max' for price.
    Works at: http://localhost:8000/recipes/recipes-by-price-set/"""

    def validate_price_params(self):
        error_msg = None
        try:
            min = Decimal(self.request.GET['min']) if 'min' in self.request.GET else Decimal('0.00')
            max = Decimal(self.request.GET['max']) if 'max' in self.request.GET else None 
        except:
            min = Decimal('0.00')
            max = None
            error_msg = {'Error': 'price should be numeric'}
        
        return min, max, error_msg

    pagination_class = PageNumberPagination

    def list(self, request):
        min, max, error_msg = self.validate_price_params()
        if error_msg:
            return Response(error_msg)
        
        queryset = Recipe.filter_by_price(min, max)

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request=request)
        if page is not None:
            serializer = RecipeSerializer(page, many=True, context={'request': request})
            paginator.template = "rest_framework/pagination/numbers.html" # doesn't help, numbers still don't show
            return paginator.get_paginated_response(serializer.data)
        
        serializer = RecipeSerializer(queryset, many=True, context={'request': request})   
        return Response(serializer.data)


