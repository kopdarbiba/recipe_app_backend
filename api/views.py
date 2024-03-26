from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from recipes.models import Recipe
from recipes.serializers import RecipeMinimalSerializer, RecipeSerializer
from recipes.utils.query_utils import annotate_total_price, get_prefetched_data

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class RecipeSearchAPIView(ListAPIView):
    """
    View to list all recipes.
    Example: http://localhost:8000/api/recipes/search/?lang=lv&ordering=total_price&q=šķēles
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeMinimalSerializer
    pagination_class = PageNumberPagination
    ordering_fields = ['total_price', 'title', 'cooking_time', 'servings']
    ordering = ['total_price']

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id','cooking_time']
    search_fields = [
        'title__name_lv', 
        'title__name_en', 
        'title__name_ru',
        'description__name_lv',
        'description__name_en',
        'description__name_ru',
        ]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = get_prefetched_data(queryset)

        # Apply client-side ordering
        ordering_param = self.request.query_params.get('ordering', self.ordering[0])

        if ordering_param:
            fields = [field.strip() for field in ordering_param.split(',')]
            # Annotate total price if ordering by total_price provided
            if 'total_price' in fields:
                queryset = annotate_total_price(queryset)
            queryset = queryset.order_by(*fields)
        return queryset
    

class RecipeList(ListAPIView):
    """
    View to list all recipes.
    Example: http://localhost:8000/api/recipes/?lang=en
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_queryset(self, *args, **kwargs):
        """
        Get method to retrieve all recipes.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = get_prefetched_data(queryset)
        return queryset

