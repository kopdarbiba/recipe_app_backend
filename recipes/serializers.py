from rest_framework import serializers

from .models import CookingMethod, CookingStepInstruction, Equipment, Ingredient, Recipe, RecipeImage, RecipeIngredient, Unit, Cuisine, Occasion, Meal
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

class CuisineSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Cuisine
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)
    
class OccasionSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Occasion
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)

class MealSerializer(LanguageMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Meal
        fields = ['name']

    def get_name(self, obj):
        return self.get_localized_field(obj)

class RecipeSerializer(LanguageMixin, serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)
    instructions = CookingStepInstructionSerializer(many=True)
    equipment = EquipmentSerializer(many = True)
    cooking_methods = CookingMethodSerializer(many = True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cuisines = CuisineSerializer(many=True)
    occasions = OccasionSerializer(many=True)
    meals = MealSerializer(many=True)
    images = ImageSerializer(many=True)        

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'cuisines',
            'occasions',
            'meals',
            'equipment',
            'cooking_methods',
            'servings',
            'instructions',
            'recipe_ingredients',
            'cooking_time',
            'calculated_total_price',
            'images',
        ]


    def get_title(self, obj) -> str:
        return self.get_localized_field(obj.title)
    
    def get_description(self, obj) -> str:
        return self.get_localized_field(obj.description)

class RecipeMinimalSerializer(LanguageMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'images',
        ]


    def get_title(self, obj):
        return self.get_localized_field(obj.title)
    
class RecipeSearchPageSerializer(LanguageMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    images = ImageSerializer(many=True)        

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'cooking_time',
            'calculated_total_price',
            'images',
        ]


    def get_title(self, obj):
        return self.get_localized_field(obj.title)