from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeImage, RecipeIngredient, Unit, CookingStepInstruction, Cuisine

class RecipeImageSerializer(serializers.ModelSerializer):

  image_url = serializers.SerializerMethodField()
  thumbnail_url = serializers.SerializerMethodField()

  class Meta:
    model = RecipeImage
    fields = ['image_url', 'thumbnail_url', 'is_main_image']

  def get_image_url(self, obj):
    return obj.generate_presigned_url_for_image()

  def get_thumbnail_url(self, obj):
    return obj.generate_presigned_url_for_thumbnail()

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name_en', 'name_lv', 'name_ru']

    def to_representation(self, instance):

        lang = self.context.get('request').query_params.get('lang', 'lv')
        lang_field = f'name_{lang}'
        name = getattr(instance, lang_field, None)
        return name

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['name_en', 'name_lv', 'name_ru']

    def to_representation(self, instance):
        lang = self.context.get('request').query_params.get('lang', 'lv')
        lang_field = f'name_{lang}'
        name = getattr(instance, lang_field, None)
        return name

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False)
    unit = UnitSerializer(many=False)
    
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

    # def to_representation(self, instance):
    #     # Print the data before serialization
    #     print("RecipeIngredient data before serialization:", instance.__dict__)

    #     # Continue with the default serialization
    #     representation = super().to_representation(instance)

    #     # Print the serialized data
    #     print("RecipeIngredient serialized data:", representation)

    #     return representation

class CookingStepInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingStepInstruction
        fields = ['step_number', 'name_en', 'name_lv', 'name_ru']
  
    def to_representation(self, instance):

        lang = self.context.get('request').query_params.get('lang', 'lv')  # Assuming default is 'lv'

        # Dynamically select the appropriate language field based on the 'lang' parameter
        lang_field = f'name_{lang}'

        # Extracting the step name using the selected language field
        step_name = getattr(instance, lang_field, None)

        return {
            'step_number': instance.step_number,
            'name': step_name,
        }
    
class CuisineSerializer(serializers.ModelSerializer):
    name_en = serializers.CharField()
    name_lv = serializers.CharField()
    name_ru = serializers.CharField()
    
    class Meta:
        model = Cuisine
        fields = ['id', 'name_en', 'name_lv', 'name_ru']


class RecipeSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cuisine = serializers.SerializerMethodField()
    occasion = serializers.SerializerMethodField()
    meal = serializers.SerializerMethodField()
    dietary_preferences = serializers.SerializerMethodField()
    images = RecipeImageSerializer(many=True, read_only=True)
    equipment = serializers.SerializerMethodField()
    cooking_methods = serializers.SerializerMethodField()
    instructions = CookingStepInstructionSerializer(many=True, read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'instructions',
            'description',
            'cuisine',
            'occasion',
            'cooking_time',
            'meal',
            'servings',
            'dietary_preferences',
            'images',
            'recipe_ingredients',
            'cooking_methods',
            'equipment',
            'calculated_total_price',
        ]

    def get_localized_field(self, obj, field_name):
        lang = self.context.get('request').query_params.get('lang', 'lv')  # Assuming default is 'lv'  
        actual_field_name = f'{field_name}_{lang}'
        return getattr(obj, actual_field_name, None)

    def get_title(self, obj):
        return self.get_localized_field(obj.title, 'name')

    def get_description(self, obj):
        return self.get_localized_field(obj.description, 'name')

    def get_cuisine(self, obj):
        return self.get_localized_field(obj.cuisine, 'name')
    
    def get_occasion(self, obj):
        return self.get_localized_field(obj.occasion, 'name')
    
    def get_meal(self, obj):
        return self.get_localized_field(obj.meal, 'name')

    def get_dietary_preferences(self, obj):
        lang = self.context.get('request').query_params.get('lang', 'lv')  # Assuming default is 'lv'
        preferences = obj.dietary_preferences.all()

        # Dynamically select the appropriate language field based on the 'lang' parameter
        lang_field = f'name_{lang}'

        # Extracting names of dietary preferences using the selected language field
        preference_names = [getattr(preference, lang_field) for preference in preferences]

        return {'diets': preference_names}

    def get_cooking_methods(self, obj):
        lang = self.context.get('request').query_params.get('lang', 'lv')  # Assuming default is 'lv'
        cooking_methods = obj.cooking_methods.all()

        # Dynamically select the appropriate language field based on the 'lang' parameter
        lang_field = f'name_{lang}'

        # Extracting cooking method names using the selected language field
        cooking_method_names = [getattr(method, lang_field, None) for method in cooking_methods]

        return {'cooking_methods': cooking_method_names}

    def get_equipment(self, obj):
        lang = self.context.get('request').query_params.get('lang', 'lv')  # Assuming default is 'lv'
        equipment = obj.equipment.all()

        # Dynamically select the appropriate language field based on the 'lang' parameter
        lang_field = f'name_{lang}'

        # Extracting equipment names using the selected language field
        equipment_names = [getattr(equipment, lang_field, None) for equipment in equipment]

        return {'equipments': equipment_names}

class RecipePreviewSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    images = RecipeImageSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'images',
        ]

    def get_localized_field(self, obj, field_name):
        lang = self.context.get('request').query_params.get('lang', 'lv')  # Assuming default is 'lv'  
        actual_field_name = f'{field_name}_{lang}'
        return getattr(obj, actual_field_name, None)

    def get_title(self, obj):
        return self.get_localized_field(obj.title, 'name')

