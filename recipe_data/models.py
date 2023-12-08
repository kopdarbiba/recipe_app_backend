# from django.db import models

# # Create your models here.



# class IngredientCategory(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class Allergen(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class Unit(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class Ingredient(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)
    
#     allergens = models.ManyToManyField(Allergen, blank=True)
#     units = models.ManyToManyField(Unit, blank=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"


# class Cuisine(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class Meal(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class Equipment(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class DietaryPreference(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

# class CookingMethod(models.Model):
#     name_eng = models.CharField(max_length=255, unique=True)
#     name_lv = models.CharField(max_length=255, unique=True)
#     name_rus = models.CharField(max_length=255, unique=True)

#     def __str__(self) -> str:
#         return f"{self.name_eng}"

