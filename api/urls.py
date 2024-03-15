from django.urls import path
from api import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<int:pk>', views.RecipeDetails.as_view()),
]