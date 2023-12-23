from django.contrib import admin
from django.db.models import Q
from .models import Recipe, RecipeIngredient, Unit, Title, Description, Ingredient, CookingMethod, Ingredient, Cuisine, CookingStepInstruction
from .models import CookingStep

# Manage unit type boolean values
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name_lv", "type_shoping_valid"]

@admin.register(Ingredient) # Search for ingredient in Recipe Ingredient
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name_eng', 'name_lv', 'name_rus']

# Ingredient selector at botmom of general info form. 
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    classes = ["collapse"]
    autocomplete_fields = ['ingredient']  # Autocomplete for ingredient
    #Filter, to show only shoping valid units
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "unit":
            kwargs["queryset"] = Unit.objects.filter(type_shoping_valid=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Text field for Cooking steps
class CookingStepInstructionInline(admin.TabularInline):
    model = CookingStepInstruction
    extra = 1
    classes = ["collapse"]
    fieldsets = (
    (None, {
            'fields': ('step_number', 'name_eng')
        }),
)

# Cooking step selector block at end of RecipeAdmin.
# Filters updates after curent form is saved ( save and continue editing)
class CookingStepsMethodInline(admin.StackedInline):
    model = CookingStep
    extra = 1
    classes = ["collapse"]
    list_filter = ('recipe_ingredients',)
    filter_horizontal = ('recipe_ingredients',)
    fieldsets = (
        (None, {
                'fields': ('step_number', 'cooking_method','recipe_ingredients')
            }),
            ('Optional Fields', {
            'classes': ('collapse',),
            'fields': ('adjective_cm', 'adjective_ri', 'adjective_alt', 'quantity', 'unit'),
        }),
    )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cooking_method":
            # Check if the recipe is being added (not saved yet)
            if "add" in request.path:
                kwargs["queryset"] = CookingMethod.objects.none()
            else:
                # Filter cooking methods based on the recipe ID
                recipe_id = request.resolver_match.kwargs.get("object_id")
                recipe = Recipe.objects.get(pk=recipe_id)
                kwargs["queryset"] = recipe.cooking_methods.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
            
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "recipe_ingredients":
            # Check if the recipe is being added (not saved yet)
            if "add" in request.path:
                kwargs["queryset"] = RecipeIngredient.objects.none()
            else:
                # Filter ingredients based on the recipe ID
                recipe_id = request.resolver_match.kwargs.get("object_id")
                if recipe_id:
                    kwargs["queryset"] = RecipeIngredient.objects.filter(recipe=recipe_id)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    
# Modify general info form, adding ingredient and cooking steps selectors at botom
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General info", {"fields": ["title", "description", "cuisine", "occasion", "meal", "cooking_time", "servings", "dietary_preferences", "equipment", "cooking_methods"], "classes": ["collapse"]}),
    ]
    
    inlines = [RecipeIngredientInline, CookingStepInstructionInline, CookingStepsMethodInline]

    # Filters for each field
    list_filter = ('dietary_preferences', 'equipment', 'cooking_methods')
    filter_horizontal = ('dietary_preferences', 'equipment', 'cooking_methods')

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

admin.site.register(Cuisine)
admin.site.register(Title)
#admin.site.register(Ingredient)
admin.site.register(Description)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Recipe, RecipeAdmin)
