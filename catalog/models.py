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

class Unit(models.Model):
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

class DietaryPreference(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class IngredientCategory(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Ingredient(models.Model):
    name_eng = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_rus = models.CharField(max_length=255, unique=True)
    allergens = models.ManyToManyField(Allergen, blank=True)
    units = models.ManyToManyField(Unit, blank=True)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    cooking_time = models.PositiveIntegerField()  # in minutes
    servings = models.PositiveIntegerField()
    instructions = models.TextField()
    nutritional_information = models.JSONField()
    
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)

    equipment = models.ManyToManyField(Equipment)
    dietary_preferences = models.ManyToManyField(DietaryPreference)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    ingredient_substitutes = models.ManyToManyField(Ingredient, related_name='substitutes', blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    # @property
    # def xl_servings(self):
    #     return "%.2f" %(float(self.servings) * 0.5)
    
    # def get_discount(self):
    #     return "qweqweqweqe"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.name_eng}"

    
# class UserIngredient(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
