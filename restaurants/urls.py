from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantViewset, GuestViewset, get_guest

router = DefaultRouter(trailing_slash=False)
router.register(r'restaurant', RestaurantViewset, basename='restaurants')
router.register(r'pos', GuestViewset, basename='restaurants')

urlpatterns = [
    path('', include(router.urls)),
    path('group/', get_guest),
]