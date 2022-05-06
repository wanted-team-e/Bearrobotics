import pytest, json  

from django.urls import reverse

pytestmark = pytest.mark.django_db

base_url = reverse('pos-list') # api/pos

post_data = {'restaurant':'1', 'price':'10000', 'number_of_party':'2', 'timestamp':'2019-12-12 03:03:03', 'payment':'CARD'}

def test_list(client):
    response = client.get(base_url)
    assert response.status_code == 200


def test_create(client):
    request = client.post(path=base_url, data=post_data)
    assert request.status_code == 201


def test_retrieve_detail(client):
    detail_url = reverse('restaurants-detail', kwargs={'pk':'1'})
    response = client.get(detail_url)
    assert response.status_code == 200


def test_put_detail(client):
    detail_url = reverse('restaurants-detail', kwargs={'pk':'1'})
    response = client.put(path=detail_url, data= \
        {'restaurant':'1', 'price':'50000', 'number_of_party':'5', 'timestamp':'2022-02-23 13:14', 'payment':'CARD'})
    assert response.status_code == 200
    assert json.loads(response.content) == {'restaurant':'1', 'price':'50000', 'number_of_party':'5', 'timestamp':'2022-02-23 13:14', 'payment':'CARD'}


def test_delete_detail(client):
    detail_url = reverse('restaurants-detail', kwargs={'pk':'11'})
    response1 = client.delete(detail_url)
    response2 = client.get(detail_url)
    assert response1.status_code == 204
    assert response2.status_code == 404


def test_retrieve_totalPrice(client):
    detail_url = reverse('restaurants-detail', args=['total_price'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url)
    assert response.status_code == 200


def test_retrieve_payment(client):
    detail_url = reverse('restaurants-detail', args=['payment'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url)
    assert response.status_code == 200


def test_retrieve_party(client):
    detail_url = reverse('restaurants-detail', args=['party'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url)
    assert response.status_code == 200