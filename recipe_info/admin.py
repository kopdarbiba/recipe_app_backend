from django.contrib import admin
from .models import GenInfo, RecipeIngredient, Unit, Title, Description, RecipeCookingMethod, Ingredient, CookingMethod
from .models import Recipe

# Manage unit type boolean values
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name_lv", "type_shoping_valid"]

# Ingredient selector for general info form. Filter, to show only shoping valid units
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "unit":
            kwargs["queryset"] = Unit.objects.filter(type_shoping_valid=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Modify general info form, adding ingredient selector at botom
class RecipeGenInfoAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_filter = ('dietary_preferences', 'equipment', 'cooking_method')
    filter_horizontal = ('dietary_preferences', 'equipment', 'cooking_method')
    

class RecipeCookingMethodInLine(admin.TabularInline):
    model = RecipeCookingMethod
    extra = 1


admin.site.register(Title)
admin.site.register(Description)
admin.site.register(Unit, UnitAdmin)
admin.site.register(GenInfo, RecipeGenInfoAdmin)

###########################################################################################################################

class RecipeCookingMethodAdmin(admin.ModelAdmin): # New page and lists fields (delete later)
    list_display = ["ingredient", "recipe", "cooking_method"]

admin.site.register(RecipeCookingMethod, RecipeCookingMethodAdmin)


# class GenInfoInline(admin.TabularInline):
#     model = GenInfo
#     extra = 1

# class RecipeAdmin(admin.ModelAdmin):
#     inline = [GenInfoInline]

# admin.site.register(Recipe, RecipeAdmin)

