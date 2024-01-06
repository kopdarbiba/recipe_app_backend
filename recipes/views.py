from django.shortcuts import render
from django.http import JsonResponse
from .models import Recipe

def get_recipe_price(request, recipe_id):
    # Fetch the recipe by ID
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        price = recipe.get_price()
        return JsonResponse({'recipe_id': recipe_id, 'total_price': price})
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)
