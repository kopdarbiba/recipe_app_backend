from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Meal(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Equipment(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Allergen(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_allergen = models.BooleanField(default=False)
    allergens = models.ManyToManyField(Allergen, blank=True)
    units = models.ManyToManyField(Unit, blank=True)
    calories = models.PositiveIntegerField()  # Calories per unit of the ingredient

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)
    cooking_time = models.PositiveIntegerField()  # in minutes
    equipment = models.ManyToManyField(Equipment)
    servings = models.PositiveIntegerField()
    instructions = models.TextField()
    dietary_preferences = models.ManyToManyField('DietaryPreference')
    nutritional_information = models.JSONField()
    ingredient_substitutes = models.ManyToManyField(Ingredient, related_name='substitutes', blank=True)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)

class DietaryPreference(models.Model):
    name = models.CharField(max_length=255, unique=True)

# class UserIngredient(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
