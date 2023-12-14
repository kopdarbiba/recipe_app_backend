from django.contrib import admin
from .models import Recipe, RecipeIngredient, Unit, Title, Description, Ingredient, CookingMethod
from .models import IngredientCookingMethod


class IngredientCookingMethodInline(admin.TabularInline):
    model = IngredientCookingMethod
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            # print(db_field.name)
            if db_field.name == "recipe":
                # Check if the RecipeNextForm is being added or changed
                print("********************")
                if "object_id" in request.resolver_match.kwargs:
                    # Access the parent RecipeNextForm object ID
                    id = request.resolver_match.kwargs["object_id"]
                    print(id)
            #         kwargs["queryset"] = RecipeNextForm.objects.filter(id=id)
            #     else:
            #         # The RecipeNextForm is being added, so we don't have an ID yet
            #         kwargs["queryset"] = RecipeNextForm.objects.none()

            # if db_field.name == "ingredient":
            #     # Use the current RecipeNextForm object ID dynamically
            #     kwargs["queryset"] = RecipeIngredient.objects.filter(recipe=request.resolver_match.kwargs.get("object_id"))

            # if db_field.name == "cooking_method":
            #     # Use the current RecipeNextForm object ID dynamically
            #     kwargs["queryset"] = CookingMethod.objects.filter(recipe=request.resolver_match.kwargs.get("object_id"))

            # return super().formfield_for_foreignkey(db_field, request, **kwargs)







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
    inlines = [RecipeIngredientInline, IngredientCookingMethodInline]

    # Filters for each field
    list_filter = ('dietary_preferences', 'equipment', 'cooking_method')
    filter_horizontal = ('dietary_preferences', 'equipment', 'cooking_method')
    
    

admin.site.register(Title)
admin.site.register(Description)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Recipe, RecipeAdmin)

###########################################################################################################################

