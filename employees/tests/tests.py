import pytest, json
from rest_framework.test import APIClient
from django.urls import reverse

pytestmark = pytest.mark.django_db

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



def test_get_user_list(client, get_confirm_user_headers):
    url = reverse('users-list')
    response = client.get(path=url, **get_confirm_user_headers)
    print(response)
    assert response.status_code == 200