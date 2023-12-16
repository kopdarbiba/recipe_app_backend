from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

@api_view(['GET'])
def get_recipe(request):
    # Get the 'recipe_id' from the request's query parameters
    recipe_id = request.GET.get('recipe_id')

    # Check if 'recipe_id' is provided
    if recipe_id is not None:
        # Try to get the Recipe instance with the specified ID; raise 404 if not found
        instance = get_object_or_404(Recipe, id=recipe_id)

        # Serialize the Recipe instance using the RecipeSerializer
        serializer = RecipeSerializer(instance)
        serialized_data = serializer.data

        # Return the serialized data as a response
        return Response(serialized_data)

    # Return an empty response if 'recipe_id' is not provided
    return Response({})
