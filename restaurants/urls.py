from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurants.views import *
from .import views

router = DefaultRouter(trailing_slash=False)
router.register('guest', views.GuestViewset)
router.register(r'restaurant', RestaurantViewset, basename='restaurants')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('group/', get_guest,),
    path(r'^group/(?P<group_name>[\w-][0-9]{4})/$', get_certain_group_list),
]