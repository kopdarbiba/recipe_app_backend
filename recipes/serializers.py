from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient, Unit

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name_eng', 'name_lv','name_rus']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['name_eng', 'name_lv','name_rus']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    unit = UnitSerializer()
    
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']


class RecipeSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cuisine = serializers.SerializerMethodField()
    meal = serializers.SerializerMethodField()
    dietary_preferences = serializers.SerializerMethodField()
    equipments = serializers.SerializerMethodField()
    cooking_methods = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)



    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'cuisine',
            'meal',
            'cooking_time',
            'servings',
            'dietary_preferences',
            'equipments',
            'cooking_methods',
            'ingredients',
        ]


    def get_title(self, obj):
        eng = obj.title.name_eng
        lv = obj.title.name_lv
        rus = obj.title.name_rus
        return {'name_eng': eng, 'name_lv': lv, 'name_rus': rus}

    def get_description(self, obj):
        eng = obj.description.name_eng
        lv = obj.description.name_lv
        rus = obj.description.name_rus
        return {'name_eng': eng, 'name_lv': lv, 'name_rus': rus}

    def get_cooking_methods(self, obj):
        cooking_methods = obj.cooking_methods.all()
        cooking_methods_info = []
        for method in cooking_methods:
            method_info = {
                'id': method.id,
                'name_eng': method.name_eng,
                'name_lv': method.name_lv,
                'name_rus': method.name_rus
            }
            cooking_methods_info.append(method_info)

        return {'equipment': cooking_methods_info}

    def get_equipments(self, obj):
        equipments = obj.equipment.all()
        equipments_info = []
        for equipment in equipments:
            equipment_info = {
                'id': equipment.id,
                'name_eng': equipment.name_eng,
                'name_lv': equipment.name_lv,
                'name_rus': equipment.name_rus
            }
            equipments_info.append(equipment_info)

        return {'equipment': equipments_info}

    def get_dietary_preferences(self, obj):
        preferences = obj.dietary_preferences.all()

        preferences_info = []
        for preference in preferences:
            preference_info = {
                'id': preference.id,
                'name_eng': preference.name_eng,
                'name_lv': preference.name_lv,
                'name_rus': preference.name_rus
            }
            preferences_info.append(preference_info)

        return {'preferences': preferences_info}

    def get_meal(self, obj):
        a = obj.dietary_preferences.all()
        print(a)
        eng = obj.meal.name_eng
        lv = obj.meal.name_lv
        rus = obj.meal.name_rus
        return {'name_eng': eng, 'name_lv': lv, 'name_rus': rus}

    def get_cuisine(self, obj):
        eng = obj.cuisine.name_eng
        lv = obj.cuisine.name_lv
        rus = obj.cuisine.name_rus
        return {'name_eng': eng, 'name_lv': lv, 'name_rus': rus}

        
    # def get_ingredients(self, obj):
    #      # Get all ingredient substitutes related to the current Recipe (obj)
    #     substitutes = obj.ingredient_substitutes.all()

    #     # Create a list to store information about each substitute ingredient
    #     substitutes_info = []
    #     for substitute in substitutes:
    #         substitute_info = {
    #             'id': substitute.id,
    #             'name_eng': substitute.name_eng,
    #             'name_lv': substitute.name_lv,
    #             'name_rus': substitute.name_rus
    #         }
    #         substitutes_info.append(substitute_info)

    #     # Return a dictionary containing information about ingredients and substitutes
    #     return {'ingredient_substitutes': substitutes_info}

