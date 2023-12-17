from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from recipes.models import CookingStep, Recipe
from recipes.serializers import CookingStepSerializer, RecipeSerializer

@api_view(['GET'])
def get_recipe(request):
    # Get the 'recipe_id' from the request's query parameters
    recipe_id = request.GET.get('recipe_id')
    if recipe_id is not None:
        # Try to get the Recipe instance with the specified ID; raise 404 if not found
        recipe_instance = get_object_or_404(Recipe, id=recipe_id)
        
        # Use filter to get all CookingStep instances related to the specified recipe_id
        cooking_steps_queryset = CookingStep.objects.filter(recipe_id=recipe_id)
        
        # Serialize the Recipe instance using the RecipeSerializer
        recipe_serializer = RecipeSerializer(recipe_instance)
        serialized_recipe_data = recipe_serializer.data

        # Serialize the list of CookingStep instances using the CookingStepSerializer
        cooking_steps_serializer = CookingStepSerializer(cooking_steps_queryset, many=True)
        serialized_cooking_steps_data = cooking_steps_serializer.data

        # Combine the serialized data for Recipe and CookingStep
        response_data = {
            'recipe': serialized_recipe_data,
            'cooking_steps': serialized_cooking_steps_data,
        }

        # Return the combined serialized data as a response
        return Response(response_data)

    # Return an empty response if 'recipe_id' is not provided
    return Response({})
