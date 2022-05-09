import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

user_login_data = {
    'email': 'kid@gmail.com',
    'password': 'Pqweasd31!'
}


def test_get_user_list(client, get_confirm_user_headers):
    url = reverse('users-list')
    response = client.get(path=url, **get_confirm_user_headers)
    assert response.status_code == 200


def test_get_user_retrieve(client, get_confirm_user_headers):
    url = reverse('users-detail', kwargs={'pk': '1'})
    response = client.get(path=url, **get_confirm_user_headers)
    assert response.status_code == 200


def test_user_login(client, get_confirm_user_headers):
    url = 'http://127.0.0.1/api/users/login'
    response = client.post(path=url, data=user_login_data)
    assert response.status_code == 200


def test_user_delete(client, get_confirm_user_headers):
    url = reverse('users-detail', kwargs={'pk': '1'})
    response = client.delete(path=url, **get_confirm_user_headers)
    assert response.status_code == 204