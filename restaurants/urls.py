from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantViewSet, GuestViewSet, get_guest, get_certain_group_list, get_city_list
from restaurants.views.menu_view import MenuViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'restaurant', RestaurantViewSet, basename='restaurants')
router.register(r'pos', GuestViewSet, basename='guests')
menu_router = DefaultRouter(trailing_slash=False)
menu_router.register(r'menu', MenuViewSet, basename='menu')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(menu_router.urls)),
]

urlpatterns += [
    path('group/', get_guest, name='group'),
    path('group/<str:group_name>/', get_certain_group_list, name='group-name'),
    path('address/<str:city_name>', get_city_list, name='address'),
]