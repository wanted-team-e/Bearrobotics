import pytest, json

from django.urls import reverse

pytest_mark = pytest.mark.django_db

base_url = reverse('users')

user_detail_data = {
    "email": "ed22c@naver.com",
    "password": "gudwns22",
    "username": "aasdasdasd",
    "rank_type": "NORMAL",
    "group": 1
}
user_signup_data = {
    "email": "ed22c@naver.com",
    "password": "gudwns22",
    "username": "aasdasdasd",
}
user_login_data = {
    "email": "ed22c@naver.com",
    "password": "gudwns22",
}
