# from django.db import models
# from django.db.models import Sum, F, Q
# from django.db.models.functions import Coalesce
# from decimal import Decimal

# class RecipeQuerySet(models.QuerySet):
#     """
#     A custom QuerySet for Recipe model.
#     """
    
#     def prefetch_and_select_related(self):
#         """
#         Return a new QuerySet instance that will prefetch and select related fields.
        
#         Returns:
#             QuerySet: A new QuerySet instance with the prefetched and selected related fields.
#         """
#         # Define the related fields to prefetch
#         prefetch_lookups = [
#             'images', 
#             'instructions', 
#             'equipment',
#             'cooking_methods',
#             'recipe_ingredients',
#             'recipe_ingredients__ingredient'  # Add 'recipe_ingredients__ingredient' to the prefetch lookups
#         ]
        
#         # Select related fields including title, description, cuisine, occasion, and meal
#         select_related_fields = [
#             'title',
#             'description',
#             'cuisine',
#             'occasion',
#             'meal'
#         ]
        
#         # Perform prefetch and select related in a single call
#         return self.prefetch_related(*prefetch_lookups).select_related(*select_related_fields)

#     def search(self, query):
#         """
#         Searches for recipes based on the provided query.

#         Args:
#             query (str): The search query.

#         Returns:
#             QuerySet: A queryset containing the filtered recipes.
#         """
#         lookup = (
#             Q(title__name_lv__icontains=query) |
#             Q(title__name_en__icontains=query) |
#             Q(title__name_ru__icontains=query) |
#             Q(description__name_lv__icontains=query) |
#             Q(description__name_en__icontains=query) |
#             Q(description__name_ru__icontains=query)
#         )

#         qs = (
#             self.prefetch_and_select_related()
#             .filter(lookup)
#         )
#         return qs
    
# class RecipesManager(models.Manager):
#     """
#     Manager for the Recipe model.
#     """
    
#     def get_queryset(self):
#         """
#         Get the QuerySet for Recipe model.
        
#         Returns:
#             RecipeQuerySet: QuerySet for Recipe model.
#         """
#         return RecipeQuerySet(self.model, using=self._db)

#     def search(self, query):
#         return self.get_queryset().search(query)
    

