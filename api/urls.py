from django.urls import path
from api import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view(), name='recipe-list'),
    path('recipes/search/', views.RecipeSearchAPIView.as_view(), name='recipe-search'),
    path('recipes/<int:pk>/', views.RecipeDetails.as_view(), name='recipe-detail'),
]