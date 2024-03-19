from django.urls import path
from api import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view(), name='recipe-list'),
    path('recipes/filter/', views.RecipeFilterList.as_view(), name='recipe-filter-list'),
    # path('recipes/<int:pk>', views.RecipeDetails.as_view(), name='recipe-detail'),
]