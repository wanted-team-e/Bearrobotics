from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantViewset

router = DefaultRouter(trailing_slash=False)
router.register(r'restaurant', RestaurantViewset, basename='restaurants')

urlpatterns = [
    path('', include(router.urls)),
]
