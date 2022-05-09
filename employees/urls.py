from django.urls import path, include
from rest_framework.routers import SimpleRouter

from employees.views import UserViewSet

user_router = SimpleRouter(trailing_slash=False)
user_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(user_router.urls)),
]