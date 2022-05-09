import pytest
from config import settings
from rest_framework.test import APIClient
from django.core.management import call_command

from restaurants.tests.factories import GroupFactory, RestaurantFactory, GuestFactory, MenuFactory
from pytest_factoryboy import register


"""
    작성자 : 김채욱
"""


register(GroupFactory)
register(RestaurantFactory)
register(GuestFactory)
register(MenuFactory)


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'testdata.json')


@pytest.fixture()
def client():
    return APIClient()



