from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view

from catalog.models import Recipe  # Import your Recipe model
from catalog.serializers import RecipeSerializer

@api_view(["GET"])
def api_home(request):
    """
    DRF API View
    """
    # Example http://127.0.0.1:8000/api/?recipe_id=2
    # http://127.0.0.1:8000/api/?recipe_id=1&field=title,%20ingredients,%20cuisine,%20meal,%20cooking_time,%20servings,%20instructions,%20nutritional_information
    # http://127.0.0.1:8000/api/?recipe_id=1&field=title
    # problem is with: ingredient_substitutes, dietary_preferences, equipment
    recipe_id = request.GET.get('recipe_id')
    field = request.GET.get('field')

    if recipe_id is not None:
        instance = get_object_or_404(Recipe, id=recipe_id)
        # data = model_to_dict(instance, fields=['id' , 'title', 'xl_servings'])  # You can specify fields=['id', 'instructions', 'servings'] if needed
        data = RecipeSerializer(instance).data
        print(data)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return Response(data)
