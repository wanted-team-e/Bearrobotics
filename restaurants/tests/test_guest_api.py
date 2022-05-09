import pytest, json

from django.urls import reverse

pytestmark = pytest.mark.django_db

base_url = reverse('guests-list')  # api/pos

data_restaurant = {'name': '비비고', 'city': '서울', 'address': '관악구 서울대입구', 'group': '1'}
data_post = {'timestamp':'2023-11-11 11:11', 'restaurant':'21','price':'20000','number_of_party':'2','payment':'CARD'}


def test_list(client, get_confirm_user_headers):
    response = client.get(base_url, **get_confirm_user_headers)
    assert response.status_code == 200


def test_create(client, get_confirm_user_headers):
    request = client.post(path=base_url, data=data_post, **get_confirm_user_headers)
    assert request.status_code == 201


def test_retrieve_detail(client, get_confirm_user_headers):
    detail_url = reverse('guests-detail', kwargs={'pk': '1'})
    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200


def test_put_detail(client, get_confirm_user_headers):
    detail_url = reverse('guests-detail', kwargs={'pk': '1'})
    response = client.put(path=detail_url, data= \
        {'timestamp':'2023-11-11 11:11', 'restaurant':'21','price':'10000','number_of_party':'2','payment':'CARD'}, 
            **get_confirm_user_headers)
    assert response.status_code == 200
    assert json.loads(response.content) == {'restaurant': 21, 'price': 10000, 'number_of_party': 2, 'timestamp': '2023-11-11T11:11:00', 'payment': 'CARD'}


def test_delete_detail(client, get_confirm_user_headers):
    detail_url = reverse('guests-detail', kwargs={'pk': '11'})
    response1 = client.delete(detail_url, **get_confirm_user_headers)
    response2 = client.get(detail_url, **get_confirm_user_headers)
    assert response1.status_code == 204
    assert response2.status_code == 404


def test_retrieve_totalPrice(client, get_confirm_user_headers):
    detail_url = reverse('guests-detail', args=['total_price'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200


def test_retrieve_payment(client, get_confirm_user_headers):
    detail_url = reverse('guests-detail', args=['payment'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200


def test_retrieve_party(client, get_confirm_user_headers):
    detail_url = reverse('guests-detail', args=['party'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200
