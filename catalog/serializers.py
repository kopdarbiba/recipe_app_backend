from rest_framework import serializers
from .models import Recipe, RecipeIngredient

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'title',
            'ingredients',
            'ingredient_substitutes',
            # 'cuisine',
            # 'meal',
            # 'cooking_time',
            # 'equipment',
            # 'servings',
            # 'instructions',
            # 'dietary_preferences',
            # 'nutritional_information',
        ]

    def get_ingredients(self, obj):
        # Assuming you have a related field named 'ingredients' in your Recipe model
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        ingredients = [{'name': recipe_ingredient.ingredient.name_eng, 'quantity': recipe_ingredient.quantity, 'unit': recipe_ingredient.unit.name_eng} for recipe_ingredient in recipe_ingredients]

        substitutes = obj.ingredient_substitutes.all()
        substitutes_info = [{'id': substitute.id, 'name': substitute.name_eng} for substitute in substitutes]

        return {'ingredients': ingredients, 'ingredient_substitutes': substitutes_info}
