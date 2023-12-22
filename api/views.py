from rest_framework.generics import ListAPIView

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
                queryset = queryset.filter(cuisine__name_eng__icontains=cuisine_name)
            if meal_name:
                queryset = queryset.filter(meal__name_eng__icontains=meal_name)

            for ingredient_name in ingredient_names:
                queryset = queryset.filter(ingredients__ingredient__name_eng__icontains=ingredient_name)

            for preference in dietary_preferences:
                queryset = queryset.filter(dietary_preferences__name_eng__icontains=preference)

            for equipment_name in equipment_names:
                queryset = queryset.filter(equipment__name_eng__icontains=equipment_name)

            for cooking_method in cooking_methods:
                queryset = queryset.filter(cooking_methods__name_eng__icontains=cooking_method)

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
                queryset = queryset.filter(ingredients__ingredient__name_eng__icontains=ingredient_name)

            return queryset.distinct()

        return Recipe.objects.none()



# @api_view(['GET'])
# def get_all_recipes(request):
#     recipes = Recipe.objects.all()
#     serializer = RecipeSerializer(recipes, many=True)
#     return Response(serializer.data)
