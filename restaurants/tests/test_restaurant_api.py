import pytest, json

from django.urls import reverse

pytestmark = pytest.mark.django_db

base_url = reverse('restaurants-list')  # api/restaurant

post_data = {'name': '비비고', 'city': '서울', 'address': '관악구 서울대입구', 'group': '1'}


def test_list(client, headers):
    response = client.get(path=base_url, **headers)
    assert response.status_code == 200


def test_create(client, headers):
    request = client.post(path=base_url, data=post_data, **headers)
    print(json.loads(request.content))
    assert request.status_code == 403


def test_retrieve_detail(client, headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    response = client.get(detail_url)
    assert response.status_code == 401
    assert json.loads(response.content) == {'name': '비비고', 'city': '서울', 'address': '서초구 서초동', 'group_name': '그룹1'}


def test_put_detail(client, headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    response = client.put(path=detail_url, data={'name': '비비빅', 'city': '부산', 'address': '서초구 서초동', 'group': 1})
    assert response.status_code == 200
    assert json.loads(response.content) == {'name': '비비빅', 'city': '부산', 'address': '서초구 서초동', 'group': 1}


def test_delete_detail(client, headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    response1 = client.delete(detail_url)
    response2 = client.get(detail_url)
    assert response1.status_code == 204
    assert response2.status_code == 404


def test_retrieve_totalPrice(client, headers):
    detail_url = reverse('restaurants-detail', args=['total_price'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url, headers)
    assert response.status_code == 200
    assert json.loads(response.content)[0] == {'restaurant_id': 21, 'day': 23, 'total_price': 40000}


def test_retrieve_payment(client, headers):
    detail_url = reverse('restaurants-detail', args=['payment'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url)
    assert response.status_code == 200
    assert json.loads(response.content)[0] == {'restaurant_id': 21, 'payment': 'BITCOIN', 'day': 24, 'count': 1}


def test_retrieve_party(client, headers):
    detail_url = reverse('restaurants-detail', args=['party'])
    parameters = '?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url)
    assert response.status_code == 200
    assert json.loads(response.content)[0] == {'number_of_party': 2, 'day': 23, 'restaurant_id': 21, 'count': 2}


def test_list_group(client, headers):
    response = client.get(path='http://127.0.0.1:8000/api/group')
    print(json.loads(response.content))
    assert response.status_code == 200


def test_retrieve_name(client, headers):
    response = client.get('http://127.0.0.1:8000/api/group/서울')
    assert response.status_code == 200
