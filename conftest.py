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


@pytest.fixture()
def headers(client):
    url = 'http://127.0.0.1:8000/api/users/signup'
    u_data = {'email':'kid@gmail.com', 'password':'Pqweasd31!','username':'dstranger'}
    request = client.post(path=url, data=u_data)
    headers = request.data['access_token']
    headers = {'HTTP_Authorization': f'Bearer "{headers}"'}
    return headers
