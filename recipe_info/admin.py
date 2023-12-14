from django.contrib import admin
from .models import Recipe, RecipeIngredient, Unit, Title, Description, RecipeCookingMethod, Ingredient, CookingMethod



# Manage unit type boolean values
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name_lv", "type_shoping_valid"]

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
    inlines = [RecipeIngredientInline]

    # Filters for each field
    list_filter = ('dietary_preferences', 'equipment', 'cooking_method')
    filter_horizontal = ('dietary_preferences', 'equipment', 'cooking_method')
    
    

admin.site.register(Title)
admin.site.register(Description)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Recipe, RecipeAdmin)

###########################################################################################################################

class RecipeCookingMethodInLine(admin.TabularInline):
    model = RecipeCookingMethod
    extra = 1

class RecipeCookingMethodAdmin(admin.ModelAdmin): # New page and lists fields (delete later)
    list_display = ["ingredient", "recipe", "cooking_method"]

admin.site.register(RecipeCookingMethod, RecipeCookingMethodAdmin)
