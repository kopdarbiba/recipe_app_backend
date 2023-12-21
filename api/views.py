from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from recipes.models import CookingStep, Recipe, RecipeIngredient
from recipes.serializers import CookingStepSerializer, RecipeSerializer

@api_view(['GET'])
def get_all_recipes(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    if recipe_id is not None:
        recipe_instance = get_object_or_404(Recipe, id=recipe_id)
        cooking_steps_queryset = CookingStep.objects.filter(recipe_id=recipe_id)

        recipe_serializer = RecipeSerializer(recipe_instance)
        serialized_recipe_data = recipe_serializer.data

        cooking_steps_serializer = CookingStepSerializer(cooking_steps_queryset, many=True)
        serialized_cooking_steps_data = cooking_steps_serializer.data

        response_data = {
            'recipe': serialized_recipe_data,
            'cooking_steps': serialized_cooking_steps_data,
        }

        return Response(response_data)

    return Response({})

class RecipesByIngredientView(ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        ingredient_name = self.request.GET.get('ingredient_name')
        print(f"Ingredient Name: {ingredient_name}")

        if ingredient_name is not None:
            recipe_ids = RecipeIngredient.objects.filter(ingredient__name_eng__iexact=ingredient_name).values_list('recipe_id', flat=True)
            print(f"Recipe IDs: {recipe_ids}")
            queryset = Recipe.objects.filter(id__in=recipe_ids)
            print(f"Queryset: {queryset}")
            return queryset

        return Recipe.objects.none()


