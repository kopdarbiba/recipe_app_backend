from rest_framework import serializers

from .models import CookingMethod, CookingStepInstruction, Equipment, Ingredient, Recipe, RecipeImage, RecipeIngredient, Unit

class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    allergen = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'allergen', 'category']

    def get_name(self, obj):
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""
    
    def get_allergen(self, obj):
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""
        
    def get_category(self, obj):
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""
class UnitSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Unit
        fields = ['type_shoping_valid', 'name']

    def get_name(self, obj):
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""
        
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
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""
        
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
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""


class CookingMethodSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CookingMethod
        fields = ['name']
    
    def get_name(self, obj):
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""

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
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""

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
    description = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'servings',
            'calculated_total_price',
            # 'instructions',
        ]

    def fetch_lang(self, obj) -> str:
        """
        Fetches the language-specific attribute value from the object.
        """
        lang_param = self.context['request'].GET.get('lang')
        if lang_param:
            str_value = getattr(obj, lang_param, None)
            if str_value is not None:
                return str_value
        # Return a default value or handle the case where lang_param is not found
        return ""

    def get_title(self, obj) -> str:
        """
        Gets the title in the specified language.
        """
        return self.fetch_lang(obj.title)

    def get_description(self, obj) -> str:
        """
        Gets the description in the specified language.
        """
        return self.fetch_lang(obj.description)
    