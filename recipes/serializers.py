from rest_framework import serializers

from .models import CookingMethod, CookingStepInstruction, Equipment, Ingredient, Recipe, RecipeImage, RecipeIngredient, Unit

class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    allergen = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'allergen', 'category']

    def get_name(self, obj) -> str:
        return getattr(obj, self.context['lang_field_name'])
    
    def get_allergen(self, obj):
        if not obj.allergen:
            return None
        else:
            return getattr(obj.allergen, self.context['lang_field_name'])

    def get_category(self, obj):
        if not obj.category:
            return None
        else:
            return getattr(obj.category, self.context['lang_field_name'])

class UnitSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Unit
        fields = ['type_shoping_valid', 'name']

    def get_name(self, obj):
        if not obj:
            return None
        else:
            return getattr(obj, self.context['lang_field_name'])
        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    unit = UnitSerializer()
    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'ingredient', 'unit']

class CookingStepInstructionSerializer(serializers.ModelSerializer):
    instruction = serializers.SerializerMethodField()
    class Meta:
        model = CookingStepInstruction
        fields = ['step_number', 'instruction']

    def get_instruction(self, obj) -> str:
        return getattr(obj, self.context['lang_field_name'])

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = ['generate_presigned_url_for_thumbnail', 'generate_presigned_url_for_image']

class EquipmentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Equipment
        fields = ['name']
    
    def get_name(self, obj):
        if not obj:
            return None
        else:
            return getattr(obj, self.context['lang_field_name'])

class CookingMethodSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CookingMethod
        fields = ['name']
    
    def get_name(self, obj):
        if not obj:
            return None
        else:
            return getattr(obj, self.context['lang_field_name'])

class RecipeSerializer(serializers.ModelSerializer):
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

    def fetch_lang(self, obj) -> str:
        str_value = getattr(obj, self.context['lang_field_name'])
        return str_value

    def get_title(self, obj) -> str:
        return self.fetch_lang(obj.title)

    def get_description(self, obj) -> str:
        return self.fetch_lang(obj.description)
    
    def get_cuisine(self, obj) -> str:
        return self.fetch_lang(obj.cuisine)

    def get_occasion(self, obj) -> str:
        return self.fetch_lang(obj.occasion)

    def get_meal(self, obj) -> str:
        return self.fetch_lang(obj.meal)


class RecipeMinimalSerializer(serializers.ModelSerializer):
    # instructions = CookingStepInstructionSerializer(many=True)
    title = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'servings',
            'calculated_total_price',
            # 'instructions',
        ]

    def fetch_lang(self, obj) -> str:
        str_value = getattr(obj, self.context['lang_field_name'])
        return str_value

    def get_title(self, obj) -> str:
        return self.fetch_lang(obj.title)