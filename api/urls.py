from django.urls import path
from .views import ComplexSearchView, RecipesByIngredientView

urlpatterns = [
    path('complexSearch/', ComplexSearchView.as_view(), name='complexSearch'),
    path('findByIngredients/', RecipesByIngredientView.as_view(), name='findByIngredients'),
]
