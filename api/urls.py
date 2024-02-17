from django.urls import path

from .views import ComplexSearchView, RecipesByIngredientView
from .views import RecipeByPriceViewSet

urlpatterns = [
    path('complexSearch/', ComplexSearchView.as_view(), name='complexSearch'),
    path('findByIngredients/', RecipesByIngredientView.as_view(), name='findByIngredients'),
	path('recipe-by-price/', RecipeByPriceViewSet.as_view({'get': 'list'}), name='recipe')
]
