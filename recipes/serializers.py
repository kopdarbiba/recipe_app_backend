from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient, Unit, CookingStep



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

  

class CookingStepSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    cooking_method = serializers.StringRelatedField()
    unit = serializers.StringRelatedField()
    adjective_cm = serializers.StringRelatedField(many=True)
    adjective_ri = serializers.StringRelatedField(many=True)
    adjective_alt = serializers.StringRelatedField(many=True)

    class Meta:
        model = CookingStep
        fields = [
            'recipe',
            'step_number',
            'cooking_method',
            'recipe_ingredients',
            'quantity',
            'unit',
            'adjective_cm',
            'adjective_ri',
            'adjective_alt',
        ]