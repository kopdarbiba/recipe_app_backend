from django.urls import path
from .views import get_recipe, RecipesByIngredientView, get_all_recipes

urlpatterns = [
    path('get_all_recipes/', get_all_recipes, name='get_all_recipes'),
    path('get_recipe/', get_recipe, name='get_recipe'),
    path('get_recipes_by_ingredient/', RecipesByIngredientView.as_view(), name='get_recipes_by_ingredient'),
]
