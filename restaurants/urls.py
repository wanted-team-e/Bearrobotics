
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurants.views import RestaurantViewset
from .import views

router = DefaultRouter(trailing_slash=False)
router.register('guest', views.GuestViewSet)
router.register(r'restaurant', RestaurantViewset, basename='restaurants')

urlpatterns = [
    path('', include(router.urls))
]




