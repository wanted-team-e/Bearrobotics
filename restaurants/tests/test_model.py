from restaurants.models import Restaurant, Guest, Group, Menu
from restaurants.tests.factories import RestaurantFactory
import pytest


pytestmark = pytest.mark.django_db


def test_restaurant_factory(restaurant_factory):
    assert restaurant_factory is RestaurantFactory

def test_restaurant(restaurant):
    assert isinstance(restaurant, Restaurant)

@pytest.mark.parametrize('restaurant__name', ['outback'])
@pytest.mark.parametrize('group__name', ['cgv'])
def test_restaurant_name(restaurant):
    assert restaurant.name == 'outback'
    assert restaurant.group.name == 'cgv'

