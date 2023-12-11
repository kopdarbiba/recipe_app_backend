from django.db import models

from recipe_info.models import RecipeGenInfo


class IngredientCategory(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Allergen(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Unit(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class CookingMethod(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Ingredient(models.Model):
    allergen = models.ForeignKey(Allergen, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)

    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class RecipeData(models.Model):
    recipe = models.ForeignKey(RecipeGenInfo, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.recipe}"

class SelectedIngredient(models.Model):
    recipe_data = models.ForeignKey(RecipeData, on_delete=models.SET_NULL, null=True)
    ingredient = models.ManyToManyField(Ingredient)
    cooking_method = models.ManyToManyField(CookingMethod)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    unit_count = models.FloatField(null=True)
