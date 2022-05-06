import pytest  

from django.urls import reverse

from restaurants.models import Restaurant

pytestmark = pytest.mark.django_db


# Create your tests here.
def test_restaurant_get():
    obj = Restaurant.objects.get(address='서초구 서초동')
    print(obj)
    assert obj.address == '서초구 서초동'