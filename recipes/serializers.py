from rest_framework import serializers

from .models import CookingMethod, CookingStepInstruction, Equipment, Ingredient, Recipe, RecipeImage, RecipeIngredient, Unit
from recipes.utils.language import LanguageMixin

class IngredientSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    allergen = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'allergen', 'category']

    def get_name(self, obj):
        return self.get_localized_field(obj)
    
    def get_allergen(self, obj):
        return self.get_localized_field(obj)
            
    def get_category(self, obj):
        return self.get_localized_field(obj)

class UnitSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Unit
        fields = ['type_shoping_valid', 'name']

    def get_name(self, obj):
        return self.get_localized_field(obj)
        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    unit = UnitSerializer()
    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'ingredient', 'unit']

class CookingStepInstructionSerializer(LanguageMixin, serializers.ModelSerializer):
    instruction = serializers.SerializerMethodField()
    class Meta:
        model = CookingStepInstruction
        fields = ['step_number', 'instruction']

    def get_instruction(self, obj):
        return self.get_localized_field(obj)
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = ['generate_presigned_url_for_thumbnail', 'generate_presigned_url_for_image']

class EquipmentSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Equipment
        fields = ['name']
    
    def get_name(self, obj):
        return self.get_localized_field(obj)

class CookingMethodSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CookingMethod
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)

class RecipeSerializer(LanguageMixin, serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)
    instructions = CookingStepInstructionSerializer(many=True)
    images = ImageSerializer(many=True)        
    equipment = EquipmentSerializer(many = True)
    cooking_methods = CookingMethodSerializer(many = True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cuisine = serializers.SerializerMethodField()
    occasion = serializers.SerializerMethodField()
    meal = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'cuisine',
            'occasion',
            'meal',
            'equipment',
            'cooking_methods',
            'servings',
            'cooking_time',
            'instructions',
            'recipe_ingredients',
            'images',
            'calculated_total_price',
        ]


    def get_title(self, obj) -> str:
        return self.get_localized_field(obj.title)
    
    def get_description(self, obj) -> str:
        return self.get_localized_field(obj.description)
        
    def get_cuisine(self, obj) -> str:
        return self.get_localized_field(obj.cuisine)
    
    def get_occasion(self, obj) -> str:
        return self.get_localized_field(obj.occasion)
    
    def get_meal(self, obj) -> str:
        return self.get_localized_field(obj.meal)

class RecipeMinimalSerializer(LanguageMixin, serializers.ModelSerializer):
    instructions = CookingStepInstructionSerializer(many=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'servings',
            'calculated_total_price',
            'instructions',
        ]


    def get_description(self, obj):
        return self.get_localized_field(obj.description)
    
    def get_title(self, obj):
        return self.get_localized_field(obj.title)