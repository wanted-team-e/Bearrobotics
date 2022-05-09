from restaurants.models import Restaurant, Guest, Group, Menu
from restaurants.tests.factories import RestaurantFactory, GroupFactory, GuestFactory, MenuFactory
import pytest

pytestmark = pytest.mark.django_db

"""
    작성자 : 김채욱
"""


# Restaurant Model
def test_restaurant_factory(restaurant_factory):
    assert restaurant_factory is RestaurantFactory


def test_restaurant(restaurant):
    assert isinstance(restaurant, Restaurant)


@pytest.mark.parametrize('restaurant__name', ['outback'])
@pytest.mark.parametrize('group__name', ['cgv'])
def test_restaurant_name(restaurant):
    assert restaurant.name == 'outback'
    assert restaurant.group.name == 'cgv'


# Group Model
def test_group_factory(group_factory):
    assert group_factory is GroupFactory


def test_group(group):
    assert isinstance(group, Group)


@pytest.mark.parametrize('group__name', ['비비고'])
def test_group_name(group):
    assert group.name == '비비고'


# Guest Model
def test_guest_factory(guest_factory):
    assert guest_factory is GuestFactory


def test_guest(guest):
    assert isinstance(guest, Guest)


@pytest.mark.parametrize('guest__number_of_party', [9])
def test_guest_age(guest):
    assert guest.number_of_party == 9


# Menu Model
def test_menu_factory(menu_factory):
    assert menu_factory is MenuFactory


def test_menu(menu):
    assert isinstance(menu, Menu)


@pytest.mark.parametrize('menu__name', ['간장게장'])
def test_menu_name(menu):
    assert menu.name == '간장게장'
