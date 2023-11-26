import json
from django.http import JsonResponse
from django.forms import model_to_dict
from catalog.models import Recipe

def api_home(request, *args, **kwargs):

    model_data = Recipe.objects.all().order_by("?").first()
    data ={}
    if model_data:
        data = model_to_dict(model_data, fields=['id', 'servings'])
    return JsonResponse(data)