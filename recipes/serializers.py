from rest_framework import serializers

from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        # Retrieve language value from context or set a default value
        context = kwargs.get('context', {})  # Retrieve the context dictionary
        self.lang = context.get('lang', 'lv')  # Retrieve the lang value from the context or default to 'lv'
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'servings',
        ]

    def get_title(self, obj):
        lang = f'name_{self.lang}'
        return getattr(obj.title, lang)

    def get_description(self, obj):
        lang = f'name_{self.lang}'
        return getattr(obj.description, lang)
