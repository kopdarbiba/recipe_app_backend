from django.urls import path, include
from rest_framework import routers

from .views import PriceFilterDemoViewSet


router = routers.DefaultRouter()
router.register(r'price-filter-demo', PriceFilterDemoViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]