import factory
from faker import Faker

from restaurants.models import Restaurant, Group, Guest, Menu

"""
    작성자 : 김채욱
"""

fake = Faker('ko_KR')

group_name = [
    '비비고', '비비큐', '도미노피자',
    '맥도날드', '김밥천국'
]

payment_name = [
    'CARD', 'CASH', 'BITCOIN', 'PHONE'
]

menu_name = [
    '김밥', '짜장면', '떡볶이', '라면', '케밥', '피자'
]


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = fake.text(ext_word_list=group_name)


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    city = fake.administrative_unit()
    address = fake.address_detail()
    name = fake.text(ext_word_list=group_name)
    group = factory.SubFactory(GroupFactory)


class GuestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Guest

    restaurant = factory.SubFactory(RestaurantFactory)
    price = fake.random_int(10000, 100000)
    number_of_party = fake.random_int(1, 10)
    timestamp = fake.date_time()
    payment = fake.text(ext_word_list=payment_name)


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    group = factory.SubFactory(GroupFactory)
    name = fake.text(ext_word_list=menu_name)
    price = fake.random_int(1000, 10000)
