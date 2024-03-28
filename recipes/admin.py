from django.contrib import admin
from django.db.models import Q
from .models import Recipe, RecipeImage, RecipeIngredient, Unit, Title, Description, Ingredient, Ingredient, Cuisine, CookingStepInstruction, Occasion


from django.utils.html import format_html

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1
    classes = ["collapse"]
    readonly_fields = ['display_original_image', 'display_image_thumbnail']

    def display_original_image(self, instance):
        if instance.image:
            presigned_url = instance.generate_presigned_url_for_image()
            return format_html('<a href="{}" target="_blank"><img src="{}" width="70" height="70" style="cursor: pointer;" /></a>'.format(presigned_url, presigned_url))
        return 'No Image'

    def display_image_thumbnail(self, instance):
        if instance.image:
            presigned_url = instance.generate_presigned_url_for_thumbnail()
            return format_html('<a href="{}" target="_blank"><img src="{}" width="70" height="70" style="cursor: pointer;" /></a>'.format(presigned_url, presigned_url))
        return 'No Image'

    display_original_image.short_description = 'Original'
    display_image_thumbnail.short_description = 'Thumbnail'

# Manage unit type boolean values
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name_lv", "type_shoping_valid"]

@admin.register(Ingredient) # Search for ingredient in Recipe Ingredient
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name_en', 'name_lv', 'name_ru']

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
            'fields': ('step_number', 'name_en', 'name_lv', 'name_ru')
        }),
    )
    
# Modify general info form, adding ingredient and cooking steps selectors at botom
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General info", {"fields": ["title", "description", "cuisines", "occasions", "meals", "cooking_time", "servings", "dietary_preferences", "equipment", "cooking_methods"], "classes": ["collapse"]}),
    ]
    
    inlines = [RecipeIngredientInline, CookingStepInstructionInline, RecipeImageInline]

    # Filters for each field
    list_filter = ('cuisines', 'occasions', 'meals', 'dietary_preferences', 'equipment', 'cooking_methods')
    filter_horizontal = ('cuisines', 'occasions', 'meals','dietary_preferences', 'equipment', 'cooking_methods')

    def get_filtered_queryset(self, model_class, request):
        if "add" in request.path:
            return model_class.objects.filter(recipe__isnull=True)
        else:
            recipe_id = request.resolver_match.kwargs.get("object_id")
            return model_class.objects.filter(Q(recipe__isnull=True) | Q(recipe__id=recipe_id))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "title":
            kwargs["queryset"] = self.get_filtered_queryset(Title, request)
        elif db_field.name == "description":
            kwargs["queryset"] = self.get_filtered_queryset(Description, request)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Cuisine)
admin.site.register(Occasion)
admin.site.register(Title)
admin.site.register(Description)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Recipe, RecipeAdmin)
