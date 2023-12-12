from django.contrib import admin
from .models import RecipeGenInfo, RecipeIngredient, Unit


from django.contrib import admin
from .models import RecipeGenInfo, RecipeIngredient, Unit

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "unit":
            kwargs["queryset"] = Unit.objects.filter(type_shoping_valid=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class RecipeGenInfoAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
admin.site.register(RecipeGenInfo, RecipeGenInfoAdmin)




class UnitAdmin(admin.ModelAdmin):
    list_display = ["name_lv", "type_shoping_valid"]
admin.site.register(Unit, UnitAdmin)

# class RecipeIngredientAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "unit":
#             kwargs["queryset"] = Unit.objects.filter(type_shoping_valid=True)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
# admin.site.register(RecipeIngredient, RecipeIngredientAdmin)