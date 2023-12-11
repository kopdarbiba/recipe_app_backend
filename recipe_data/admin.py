from django.contrib import admin

from .models import SelectedIngredient, RecipeData



class IngredientInline(admin.TabularInline):
    model = SelectedIngredient
    extra = 1


class RecipeDataAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]

admin.site.register(RecipeData, RecipeDataAdmin)

