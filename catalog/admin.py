from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Cuisine)
admin.site.register(Meal)
admin.site.register(Equipment)
admin.site.register(Unit)
admin.site.register(Allergen)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)

