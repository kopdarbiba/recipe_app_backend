from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from django.db.models import Prefetch
from decimal import Decimal

from recipes.models import RecipeImage, RecipeIngredient

def annotate_total_price(queryset):
    return queryset.annotate(
            total_price=Coalesce(
                Sum(F('recipe_ingredients__quantity') * F('recipe_ingredients__ingredient__price'), output_field=DecimalField()),
                Decimal('0')
            )
        )

def get_prefetched_data(queryset, main_img_only=False):
    """
    Utility function to prefetch related data for recipes queryset.
    """
    # Define prefetch for recipe ingredients
    prefetched_recipe_ingredients = Prefetch(
        "recipe_ingredients",
        queryset=RecipeIngredient.objects.select_related(
            'ingredient',
            'unit',
            'ingredient__allergen',
            'ingredient__category',
        )
    )

    # Prefetch related data for the main queryset
    queryset = queryset.select_related(
        'title',
        'description',
    ).prefetch_related(
        'cuisines',
        'occasions',
        'meals',
        'instructions',
        'equipment',
        'cooking_methods',
        prefetched_recipe_ingredients,
    )

    # Prefetch main images if main_img_only is True
    if main_img_only:
        queryset = queryset.prefetch_related(
            Prefetch('images', queryset=RecipeImage.objects.filter(is_main_image=True))
        )

    return queryset
