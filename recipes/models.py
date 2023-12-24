from django.db import models

class Title(models.Model):
    name_eng = models.CharField(max_length=255)
    name_lv = models.CharField(max_length=255, null=True, blank=True)
    name_rus = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Description(models.Model):
    name_eng = models.TextField()
    name_lv = models.TextField(max_length=3000, null=True, blank=True)
    name_rus = models.TextField(max_length=3000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Cuisine(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"
    
class Occasion(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"

class Meal(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"

class Equipment(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"

class DietaryPreference(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"
    
class IngredientCategory(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"

class Allergen(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"

class CookingMethod(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"

class Unit(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)
    type_shoping_valid = models.BooleanField(null=True)
    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"

class Adjective(models.Model):
    name_eng = models.CharField(max_length=50, unique=True)
    name_lv = models.CharField(max_length=50, unique=True)
    name_rus = models.CharField(max_length=50, unique=True)
    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"
    
class Ingredient(models.Model):
    allergen = models.ForeignKey(Allergen, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)

    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self) -> str:
        return f"{self.name_eng} | {self.name_lv}"
    
class Recipe(models.Model):
    title = models.OneToOneField(Title, on_delete=models.SET_NULL, null=True)
    description = models.OneToOneField(Description, on_delete=models.SET_NULL, null=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)
    cooking_time = models.PositiveIntegerField()
    servings = models.PositiveIntegerField()
    dietary_preferences = models.ManyToManyField(DietaryPreference)
    equipment = models.ManyToManyField(Equipment)
    cooking_methods = models.ManyToManyField(CookingMethod)
    
    def __str__(self) -> str:
        return f"model Recipe: {self.title}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ingredient.name_eng}:  {self.quantity} {self.unit}" 

class CookingStepInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveSmallIntegerField()
    name_eng = models.TextField(max_length=3000, null=True, blank=True)
    name_lv = models.TextField(max_length=3000, null=True, blank=True)
    name_rus = models.TextField(max_length=3000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"
    
class CookingStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    cooking_method = models.ForeignKey(CookingMethod, on_delete=models.CASCADE)
    recipe_ingredients = models.ManyToManyField(RecipeIngredient)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    adjective_cm = models.ManyToManyField(Adjective, blank=True, related_name='adjective_cm_set')
    adjective_ri = models.ManyToManyField(Adjective, blank=True, related_name='adjective_ri_set')
    adjective_alt = models.ManyToManyField(Adjective, blank=True, related_name='adjective_alt_set')
    
    def __str__(self) -> str:
        return f"Cooking Step for {self.recipe} - {self.cooking_method}"