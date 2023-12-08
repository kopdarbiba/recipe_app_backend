# from django.db import models
    

# class Recipe(models.Model):
   
#     # cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
#     # meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)

#     # equipment = models.ManyToManyField(Equipment)
#     # dietary_preferences = models.ManyToManyField(DietaryPreference)
#     # ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
#     # ingredient_substitutes = models.ManyToManyField(Ingredient, related_name='substitutes', blank=True)
#     # cooking_methods = models.ManyToManyField(CookingMethod)

#     def __str__(self) -> str:
#         return f"{self.title}"

# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     # ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
#     # quantity = models.CharField(max_length=50)
#     # unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class CookingStep(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     step_number = models.PositiveIntegerField()
#     description = models.TextField()

#     def __str__(self) -> str:
#         return f"Step {self.step_number} for {self.recipe.title}"
