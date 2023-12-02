from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from catalog.models import Recipe  # Import your Recipe model
# from data_population.models import Ingridient

def api_home(request):
    # Example http://127.0.0.1:8000/api/?recipe_id=2
    # http://127.0.0.1:8000/api/?recipe_id=1&field=title,%20ingredients,%20cuisine,%20meal,%20cooking_time,%20servings,%20instructions,%20nutritional_information
    # problem is with: ingredient_substitutes, dietary_preferences, equipment
    recipe_id = request.GET.get('recipe_id')
    field = request.GET.get('field')

    if recipe_id is not None:
        try:
            model_data = get_object_or_404(Recipe, id=recipe_id)
            data = model_to_dict(model_data, fields=field)  # You can specify fields=['id', 'instructions', 'servings'] if needed
            print(data)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        except ValueError:
            data = {'error': 'Invalid recipe ID'}
    else:
        data = {'error': 'Recipe ID not provided in the request'}
    return JsonResponse(data)
