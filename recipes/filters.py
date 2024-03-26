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
        search_query = request.query_params.get('q', '')
        if search_query:
            search_fields = [
                'title__name_lv',
                'title__name_en',
                'title__name_ru',
                'description__name_lv',
                'description__name_en',
                'description__name_ru',
            ]
            # Build a Q object to perform case-insensitive search across multiple fields
            search_filters = Q()
            for field in search_fields:
                search_filters |= Q(**{f'{field}__icontains': search_query})
            queryset = queryset.filter(search_filters)

        min_total_price = request.query_params.get('min_price')
        max_total_price = request.query_params.get('max_price')
        if min_total_price or max_total_price:
            queryset = annotate_total_price(queryset)
            if min_total_price is not None:
                queryset = queryset.filter(total_price__gte=min_total_price)

            if max_total_price is not None:
                queryset = queryset.filter(total_price__lte=max_total_price)
        
        return queryset