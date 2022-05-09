import pytest, json

from django.urls import reverse

pytestmark = pytest.mark.django_db

base_url = reverse('restaurants-list')  # api/restaurant

data_restaurant = {'name': '비비고', 'city': '서울', 'address': '관악구 서울대입구', 'group': '1'}
data_post = {'timestamp':'2023-11-11 11:11', 'restaurant':'21','price':'20000','number_of_party':'2','payment':'CARD'}



def test_list(client, get_normal_user_headers):
    response = client.get(path=base_url, **get_normal_user_headers)
    assert response.status_code == 200


def test_create(client, get_confirm_user_headers):
    request = client.post(path=base_url, data=data_restaurant, **get_confirm_user_headers)
    print(json.loads(request.content))
    assert request.status_code == 201
    assert json.loads(request.content) == {'name': '비비고', 'city': '서울', 'address': '관악구 서울대입구', 'group': 1}


def test_retrieve_detail(client, get_confirm_user_headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200


def test_put_detail(client, get_confirm_user_headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '22'})
    response = client.put(path=detail_url, data={'name': '비비빅', 'city': '부산', 'address': '서초구 서초동', 'group': 1}, **get_confirm_user_headers)
    assert response.status_code == 200
    assert json.loads(response.content) == {'name': '비비빅', 'city': '부산', 'address': '서초구 서초동', 'group': 1}


def test_delete_detail(client, get_confirm_user_headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    response1 = client.delete(detail_url, **get_confirm_user_headers)
    response2 = client.get(detail_url, **get_confirm_user_headers)
    assert response1.status_code == 204
    assert response2.status_code == 404


def test_retrieve_totalPrice(client, get_confirm_user_headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    print(detail_url)
    parameters = '/total_price?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters
    print(detail_url)

    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200
    assert json.loads(response.content)[0] == {'restaurant_id': 21, 'day': 23, 'total_price': 40000}


def test_retrieve_payment(client, get_confirm_user_headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    print(detail_url)
    parameters = '/payment?&timeunit=day&start_time=2021-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters
    print(detail_url)

    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200
    assert json.loads(response.content)[0] == {'restaurant_id': 21, 'payment': 'BITCOIN', 'day': 24, 'count': 1}


def test_retrieve_party(client, get_confirm_user_headers):
    detail_url = reverse('restaurants-detail', kwargs={'pk': '21'})
    parameters = '/party?&timeunit=day&start_time=2022-02-23%2013:14&end_time=2022-02-28%2014:14'
    detail_url += parameters

    response = client.get(detail_url, **get_confirm_user_headers)
    assert response.status_code == 200
    assert json.loads(response.content)[0] == {'number_of_party': 2, 'day': 23, 'restaurant_id': 21, 'count': 2}


def test_list_group(client, get_normal_user_headers):
    url = reverse('group')
    response = client.get(path=url, **get_normal_user_headers)
    print(json.loads(response.content))
    assert response.status_code == 200


def test_retrieve_group(client, get_normal_user_headers):
    url = reverse('group-name', kwargs={'group_name': '그룹1'})
    response = client.get(path=url, **get_normal_user_headers)
    assert response.status_code == 200

def test_retrieve_address(client, get_normal_user_headers):
    url = reverse('address', kwargs={'city_name': '서울'})
    response = client.get(path=url, **get_normal_user_headers)
    assert response.status_code == 200