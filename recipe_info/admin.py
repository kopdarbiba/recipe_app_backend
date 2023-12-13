from django.contrib import admin
from .models import RecipeGenInfo, RecipeIngredient, Unit, CookingMethod

# Ingredient selector for general info form. Filter, to show only shoping valid units
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "unit":
            kwargs["queryset"] = Unit.objects.filter(type_shoping_valid=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Manage unit type boolean values
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name_lv", "type_shoping_valid"]

# Modify general info form, adding ingredient selector at botom
class RecipeGenInfoAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]


admin.site.register(Unit, UnitAdmin)
admin.site.register(RecipeGenInfo, RecipeGenInfoAdmin)

###########################################################################################################################

# class RecipeCookingMethodInline(admin.TabularInline):
#     model = IngredientCookingMethod
#     extra = 1

# class RecipeIngredientAdmin(admin.ModelAdmin):
#     inline = [RecipeCookingMethodInline]

# admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
