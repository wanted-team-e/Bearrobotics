from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantViewset, GuestViewset, get_guest, get_certain_group_list, get_city_list
from restaurants.views import *
from restaurants.views.menu_view import MenuViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'restaurant', RestaurantViewset, basename='restaurants')
router.register(r'pos', GuestViewset, basename='restaurants')
menu_router = DefaultRouter(trailing_slash=False)
menu_router.register(r'menu', MenuViewSet, basename='menu')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(menu_router.urls)),
]

urlpatterns += [
    path('group/', get_guest,),
    path('group/<str:group_name>/', get_certain_group_list),
    path('address/<str:city_name>', get_city_list),
]