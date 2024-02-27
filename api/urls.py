from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ComplexSearchView, RecipesByIngredientView
from .views import RecipesByPriceViewSet, RecipesViewSet
from .views import RecipesByPriceView

urlpatterns = [
    path('complexSearch/', ComplexSearchView.as_view(), name='complexSearch'),
    path('findByIngredients/', RecipesByIngredientView.as_view(), name='findByIngredients'),
	path('recipes-by-price/', RecipesByPriceView.as_view(), name='recipeByPrice'), 
	#path('recipe-by-price-list/', RecipesByPriceViewSet.as_view({'get': 'list'}), name='recipe-testing') # example, let's leave it here
]

router = DefaultRouter()
router.register(r'recipes-by-price-set', RecipesByPriceViewSet, basename='recipe')
router.register(r'recipes-set', RecipesViewSet, basename='recipesViewSet') # 

urlpatterns += router.urls 