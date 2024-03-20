from typing import Any
from django.db import models
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal


class RecipeQuerySet(models.QuerySet):
    def prefetch_and_select_related(self):
        """
        Return a new QuerySet instance that will prefetch and select related fields.
        
        Returns:
            QuerySet: A new QuerySet instance with the prefetched and selected related fields.
        """
        # Define the related fields to prefetch
        prefetch_lookups = [
            'images', 
            'instructions', 
            'equipment',
            'cooking_methods',
            'recipe_ingredients',
        ]
        
        # Add 'recipe_ingredients__ingredient' to the prefetch lookups
        prefetch_lookups += ['recipe_ingredients__ingredient']
        
        # Select related fields including title, description, cuisine, occasion, and meal
        select_related_fields = [
            'title',
            'description',
            'cuisine',
            'occasion',
            'meal'
        ]
        
        # Perform prefetch and select related in a single call
        return self.prefetch_related(*prefetch_lookups).select_related(*select_related_fields)


class ReceptesManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def manage_related(self):
        return self.get_queryset().prefetch_and_select_related()
    
    def sort_by_total_price(self):
        """
        Sort recipes by their total price.
        
        Returns:
            QuerySet: A queryset containing recipes sorted by total price.
        """
        return self.manage_related().annotate(
            total_price=Coalesce(
                Sum(F('recipe_ingredients__quantity') * F('recipe_ingredients__ingredient__price'), output_field=models.DecimalField()),
                Decimal('0')
            )
        ).order_by('total_price')

    def filter_by_price(self, queryset, min_price=None, max_price=None):
    
        """
        Filter recipes in the given queryset by price range.
        
        Args:
            queryset (QuerySet): The queryset to filter.
            min_price (Decimal, optional): The minimum price to filter by.
            max_price (Decimal, optional): The maximum price to filter by.
        
        Returns:
            QuerySet: A filtered queryset containing recipes within the specified price range.
        """
        if min_price is not None:
            queryset = queryset.filter(total_price__gte=min_price)
        
        if max_price is not None:
            queryset = queryset.filter(total_price__lte=max_price)
        
        return queryset

    def filter_by_title(self, title):
        """
        Filter recipes by title.
        
        Args:
            title (str): The title to filter by.
        
        Returns:
            QuerySet: A queryset containing recipes filtered by title name_lv.
        """
        return self.manage_related().filter(title__name_lv__icontains=title)
    