from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=150)
    servings = models.IntegerField(null=True)

    # Basic info
    description = models.TextField(null=True)
    cuisine = models.CharField(max_length=50, null=True)
    meal = models.CharField(max_length=50, null=True)
    food_category = models.CharField(max_length=50, null=True)

    # Details
    cooking_time = models.IntegerField(null=True)
    equipment = models.TextField(null=True)
    ingredient = models.TextField(null=True)
    cooking_steps = models.TextField(null=True)
    allergens = models.TextField(null=True)
    ingredient_substitute = models.TextField(null=True)

    # Nutrition
    nutritional_information = models.TextField(null=True)
    calories = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    # Rating
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)

    # Additional info
    dietary_preference = models.CharField(max_length=50, null=True)

    measurements = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    # Date and Time
    created_at = models.DateTimeField(auto_now_add=True)  # Set automatically when created
    updated_at = models.DateTimeField(auto_now=True)  # Set automatically when updated


 