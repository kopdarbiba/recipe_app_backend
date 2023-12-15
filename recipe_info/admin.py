from django.contrib import admin
from django.db.models import Q
from .models import Recipe, RecipeIngredient, Unit, Title, Description, Ingredient, CookingMethod, Ingredient
from .models import IngredientCookingMethod

# Manage unit type boolean values
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name_lv", "type_shoping_valid"]

class IngredientCookingMethodInline(admin.TabularInline):
    model = IngredientCookingMethod
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == "ingredient":
                # Check if the recipe is being added (not saved yet)
                if "add" in request.path:
                    kwargs["queryset"] = Ingredient.objects.none()
                else:
                    # Filter ingredients based on the recipe ID
                    recipe_id = request.resolver_match.kwargs.get("object_id")
                    kwargs["queryset"] = Ingredient.objects.filter(recipeingredient__recipe=recipe_id)

            if db_field.name == "cooking_method":
                # Check if the recipe is being added (not saved yet)
                if "add" in request.path:
                    kwargs["queryset"] = CookingMethod.objects.none()
                else:
                    # Filter cooking methods based on the recipe ID
                    recipe_id = request.resolver_match.kwargs.get("object_id")
                    kwargs["queryset"] = Recipe.objects.get(pk=recipe_id).cooking_method.all()

            return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Ingredient selector at botmom of general info form. 
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    #Filter, to show only shoping valid units
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "unit":
            kwargs["queryset"] = Unit.objects.filter(type_shoping_valid=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Modify general info form, adding ingredient selector at botom
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, IngredientCookingMethodInline]

    # Filters for each field
    list_filter = ('dietary_preferences', 'equipment', 'cooking_method')
    filter_horizontal = ('dietary_preferences', 'equipment', 'cooking_method')

    def get_filtered_queryset(self, model_class, request):
        if "add" in request.path:
            return model_class.objects.filter(recipe__isnull=True)
        else:
            recipe_id = request.resolver_match.kwargs.get("object_id")
            return model_class.objects.filter(Q(recipe__isnull=True) | Q(recipe__id=recipe_id)) # This is pure MAGICK!!! :D

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "title":
            kwargs["queryset"] = self.get_filtered_queryset(Title, request)
        elif db_field.name == "description":
            kwargs["queryset"] = self.get_filtered_queryset(Description, request)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Title)
admin.site.register(Ingredient)
admin.site.register(Description)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Recipe, RecipeAdmin)

###########################################################################################################################

