from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from catalog.models import Recipe  # Import your Recipe model
from data_population.models import Ingridient

def api_home(request):
    # Example http://127.0.0.1:8000/api/?recipe_id=2
    recipe_id = request.GET.get('recipe_id')

    if recipe_id is not None:
        try:
            model_data = get_object_or_404(Recipe, id=recipe_id)
            data = model_to_dict(model_data)  # You can specify fields=['id', 'instructions', 'servings'] if needed
        except ValueError:
            data = {'error': 'Invalid recipe ID'}
    else:
        data = {'error': 'Recipe ID not provided in the request'}

    return JsonResponse(data)