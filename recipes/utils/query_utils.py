# utils.py
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal

def annotate_total_price(queryset):
    return queryset.annotate(
            total_price=Coalesce(
                Sum(F('recipe_ingredients__quantity') * F('recipe_ingredients__ingredient__price'), output_field=DecimalField()),
                Decimal('0')
            )
        )