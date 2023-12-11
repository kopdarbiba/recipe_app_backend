from django.db import models


class Cuisine(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Meal(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Equipment(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class DietaryPreference(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class RecipeGenInfo(models.Model):
    title = models.CharField(max_length=255)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)
    equipment = models.ManyToManyField(Equipment)
    dietary_preferences = models.ManyToManyField(DietaryPreference)
    cooking_time = models.PositiveIntegerField()  # in minutes
    servings = models.PositiveIntegerField()
    description = models.TextField()
    nutritional_information = models.JSONField(default=dict)
    
    def __str__(self) -> str:
        return f"{self.title}"
    

