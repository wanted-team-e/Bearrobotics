import pytest, json
from rest_framework.test import APIClient
from django.urls import reverse

pytest_mark = pytest.mark.django_db

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



def set_credential():
    resp = APIClient.post(
        '127.0.0.1:8000/api/employees/signup', {'email': 'edc22c@naver.com', 'password': 'asdasd15s', 'username': '이형준'}
    )
    tokens = json.loads(resp.content)
    access_token = tokens.get('access_token', None)
    print(access_token)
    APIClient.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')


set_credential()