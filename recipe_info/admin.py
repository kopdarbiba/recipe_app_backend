from django.contrib import admin
from .models import GenInfo, RecipeIngredient, Unit
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


admin.site.register(Unit, UnitAdmin)
admin.site.register(GenInfo, RecipeGenInfoAdmin)

###########################################################################################################################

class GenInfoInline(admin.TabularInline):
    model = GenInfo
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inline = [GenInfoInline]

admin.site.register(Recipe, RecipeAdmin)

