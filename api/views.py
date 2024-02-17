from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Sum, F, Value, IntegerField, Subquery

from recipes.models import Recipe
from recipes.models import RecipeIngredient
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
    

class RecipeByPriceViewSet(viewsets.ModelViewSet):
    """API endpoint that shows recipes by price
        accepts GET params 'min' and 'max' (price)
    """
    serializer_class = RecipeSerializer

    def filter_by_price(self, min, max):
        if (max == None) and (min == 0):
            return Recipe.objects.all()
        else:
            subquery_prices = (
                RecipeIngredient.objects
                .values('recipe_id')
                .annotate(total_price=Sum(F('quantity') * F('ingredient__price')))
                .order_by('total_price')
            )
            if max != None:
                subquery_filtered_prices = subquery_prices.filter(total_price__range=[min, max])
            else:
                subquery_filtered_prices = subquery_prices.filter(total_price__gt=min)
            return (Recipe.objects.filter(id__in=Subquery(subquery_filtered_prices.values('recipe_id'))).annotate(
                total_price=Value(0, output_field=IntegerField())).annotate(
                    total_price=Subquery(subquery_filtered_prices.values('total_price')[:1]))  # Update total_price using the subquery
            )

    def list(self, request):
        try:
            min_price = float(request.GET['min']) if 'min' in request.GET else 0
            max_price = float(request.GET['max']) if 'max' in request.GET else None 
        except:
            return Response({'Error': 'price should be numeric'})
        
        queryset = self.filter_by_price(min_price, max_price)
        
        data = {}
        if queryset:
            for item in queryset:
                data[item.pk] = RecipeSerializer(item, context={'request': request}).data     
        return Response(data)
