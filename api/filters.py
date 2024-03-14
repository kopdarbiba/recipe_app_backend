from decimal import Decimal
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.db.models.fields import DecimalField

class RecipeFilter:
    @staticmethod
    def by_total_price(queryset):
        return queryset.annotate(
            total_price=Coalesce(
                Sum(F('recipe_ingredients__quantity') * F('recipe_ingredients__ingredient__price'), output_field=DecimalField()),
                Decimal('0')
            )
        ).order_by('total_price')
    
    @staticmethod
    def by_price_range(queryset, min_price=None, max_price=None):
        filters = {}

        if min_price is not None:
            filters['total_price__gte'] = min_price

        if max_price is not None:
            filters['total_price__lte'] = max_price

        return queryset.filter(**filters)

    @staticmethod
    def by_ingredients(queryset, ingredient_ids=None):
        if ingredient_ids is not None:
            filters = {'recipe_ingredients__ingredient__id__in': ingredient_ids}
            return queryset.filter(**filters)
        return queryset