from rest_framework import filters
from django.db.models import Q

from recipes.utils.query_utils import annotate_total_price

class RecipeOrderingFilter(filters.OrderingFilter):
    ordering_fields = {
        'total_price': 'total_price',
        'cooking_time': 'cooking_time',
        'servings': 'servings',
    }

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering and any(field in ordering for field in ['total_price', '-total_price']):
            # Annotate the queryset with total_price if ordering by it
            queryset = annotate_total_price(queryset)
        return super().filter_queryset(request, queryset, view)

class RecipeSearchFilter(filters.BaseFilterBackend):
    """
    Filter that performs a case-insensitive search on multiple fields.
    """

    def filter_queryset(self, request, queryset, view):
        """
        Filter the Recipe queryset based on the provided query parameters.

        Args:
            request: The request object.
            queryset: The queryset of Recipe objects.
            view: The view instance.

        Returns:
            The filtered queryset.
        """
        search_query = request.query_params.get('q', '')
        if search_query:
            search_filters = Q()
            search_fields = ['title__name_lv', 'title__name_en', 'title__name_ru',
                             'description__name_lv', 'description__name_en', 'description__name_ru']
            for field in search_fields:
                search_filters |= Q(**{f'{field}__icontains': search_query})
            queryset = queryset.filter(search_filters)

        min_total_price = request.query_params.get('min_price')
        max_total_price = request.query_params.get('max_price')

        occasions = request.query_params.get('occasions')
        meals = request.query_params.get('meals')
        cuisines = request.query_params.get('cuisines')
        ingredients = request.query_params.get('ingredients')

        # Define a helper function to filter by model field
        if occasions:
            queryset = self.filter_by_model_field(queryset, 'occasions', occasions)
        if meals:
            queryset = self.filter_by_model_field(queryset, 'meals', meals)
        if cuisines:
            queryset = self.filter_by_model_field(queryset, 'cuisines', cuisines)
        if ingredients:
            queryset = self.filter_by_model_field(queryset, 'recipe_ingredients__ingredient', ingredients)
        if min_total_price is not None or max_total_price is not None:
            queryset = self.filter_by_total_price(queryset, min_total_price, max_total_price)

        return queryset

    def filter_by_model_field(self, queryset, field_name, field_value_list):
        """
        Helper function to filter queryset by model field.

        Args:
            queryset: The queryset of Recipe objects.
            field_name: The name of the model field to filter on.
            field_value_list: The list of values to filter by.

        Returns:
            The filtered queryset.
        """
        field_values = field_value_list.split(',')  # Split comma-separated values
        for field_value in field_values:
            field_lookup = self.filter_field_value(field_name, field_value)
            queryset = queryset.filter(field_lookup)
        return queryset

    def filter_field_value(self, field_name, field_value):
        """
        Helper function to generate Q objects for filtering field values.

        Args:
            field_name: The name of the model field.
            field_value: The value to filter.

        Returns:
            Q object representing the filter condition.
        """
        field_lookup = Q()
        for lang_field in ['name_en', 'name_lv', 'name_ru']:
            field_lookup |= Q(**{f'{field_name}__{lang_field}__iexact': field_value})
        return field_lookup

    def filter_by_total_price(self, queryset, min_price, max_price):
        """
        Filter the Recipe queryset by total price range.

        Args:
            queryset: The queryset of Recipe objects.
            min_price: The minimum total price.
            max_price: The maximum total price.

        Returns:
            The filtered queryset.
        """
        queryset = annotate_total_price(queryset)
        if min_price is not None:
            queryset = queryset.filter(total_price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(total_price__lte=max_price)
        return queryset
