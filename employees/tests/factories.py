import factory
from faker import Faker

from employees.models import Employee
from restaurants.tests.factories import GroupFactory

fake = Faker('ko_KR')
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    group = factory.SubFactory(GroupFactory)
    username = fake.text(ext_word_list=menu_name)
    price = fake.random_int(1000,10000)