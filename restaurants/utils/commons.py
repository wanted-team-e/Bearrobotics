from datetime import datetime
from django.db.models import Q, Sum
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractDay, ExtractHour
from rest_framework import status

from rest_framework.response import Response

from restaurants.models import Guest, Restaurant, Group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def _request_param(request):
    """
        작성자 : 강정희
    """
    result = {
        'start_time': request.query_params.get('start_time', None),
        'end_time': request.query_params.get('end_time', None),
        'timeunit': request.query_params.get('timeunit', None),
        'min_price': request.query_params.get('min_price', None),
        'max_price': request.query_params.get('max_price', None),
        'min_party': request.query_params.get('min_party', None),
        'max_party': request.query_params.get('max_party', None),
        'group': request.query_params.get('group', None)
    }
    return result


def exception_handling(request):
    """
        작성자 : 강정희
    """
    requests = _request_param(request)

    timeunit = requests.get('timeunit')
    occurred = False
    error = ''

    query = Q(timestamp__range=(requests.get('start_time'), requests.get('end_time')))

    if requests.get('min_price') and requests.get('max_price'):
        query &= Q(price__range=(requests.get('min_price'), requests.get('max_price')))
    if requests.get('min_party') and requests.get('max_party'):
        query &= Q(number_of_party__range=(requests.get('min_party'), requests.get('max_party')))
    if requests.get('group'):
        query &= Q(restaurant__group__name=requests.get('group'))

    # request 입력값에 대한 예외처리

    if requests.get('start_date') and requests.get('end_time'):
        try:
            date_format = "%Y-%m-%d"
            datetime.strptime(requests.get('start_time'), date_format)
            datetime.strptime(requests.get('end_time'), date_format)

            if requests.get('start_time') > requests.get('end_time'):
                occurred = True
                error = Response({'error_message': "조회 시작 날짜보다 끝 날짜가 빠를 수 없습니다."},
                                 status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            occurred = True
            error = Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                               "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    if requests.get('min_price') and requests.get('max_price'):
        if not (requests.get('min_price').isdigit() or requests.get('max_price').isdigit()):
            occurred = True
            error = Response({'error_message': "조회 최소 가격, 최대 가격은 숫자값을 입력해야합니다."},
                             status=status.HTTP_400_BAD_REQUEST)
        if requests.get('min_price') > requests.get('max_price'):
            occurred = True
            error = Response({'error_message': "조회 최소 가격보다 최대 가격이 클 수 없습니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    if requests.get('min_party') and requests.get('max_party'):
        if requests.get('min_party').isdigit() or requests.get('max_party').isdigit():
            occurred = True
            error = Response({'error_message': "조회 최소 방문자 수, 최대 방문자 수는 숫자값을 입력해야합니다."},
                             status=status.HTTP_400_BAD_REQUEST)
        if requests.get('min_party') > requests.get('max_party'):
            occurred = True
            error = Response({'error_message': "조회 최소 방문자 수보다 최대 방문자 수가 클 수 없습니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    if requests.get('group'):
        group_chk = Guest.objects.filter(query).exists()

        if not group_chk:
            occurred = True
            error = Response({'error_message': "조회 그룹 이름이 존재하지 않습니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    result = {
        'timeunit': timeunit,
        'query': query,
        'occurred': occurred,
        'error': error
    }
    return result


def set_swagger():
    """
        작성자 : 김채욱
    """
    param_1 = openapi.Parameter( 'start_time', openapi.IN_QUERY, description='start time/end time(must)', type=openapi.TYPE_STRING )
    param_2 = openapi.Parameter( 'endtime', openapi.IN_QUERY, description='start time/end time(must)', type=openapi.TYPE_STRING )
    param_3 = openapi.Parameter( 'timeunit', openapi.IN_QUERY, description='aggregation time window (must)', type=openapi.TYPE_STRING )
    param_4 = openapi.Parameter( 'min_price', openapi.IN_QUERY, description='price range(optional)', type=openapi.TYPE_INTEGER )
    param_5 = openapi.Parameter( 'max_price', openapi.IN_QUERY, description='price range(optional)', type=openapi.TYPE_INTEGER )
    param_6 = openapi.Parameter( 'min_party', openapi.IN_QUERY, description='number of party(optional)', type=openapi.TYPE_INTEGER )
    param_7 = openapi.Parameter( 'max_party', openapi.IN_QUERY, description='number of party(optional)', type=openapi.TYPE_INTEGER )
    param_8 = openapi.Parameter( 'group', openapi.IN_QUERY, description='restaurant group(optional)', type=openapi.TYPE_INTEGER )

    manual_parameters = [param_1,param_2,param_3,param_4,param_5,param_6,param_7,param_8]
    return manual_parameters


def is_group_name_in_group(group_name):
    """
        작성자 : 서재환
    """
    try:
        group = Group.objects.get(name = group_name)
    except:
        return False
    return True


def get_restaurants_id(group_name):
    """
        작성자 : 서재환
    """
    restaurants = []
    restaurants_id_list = []
    group_id = Group.objects.get(name = group_name)
    restaurants = Restaurant.objects.filter(group_id=group_id)
    if len(restaurants) == 0:
        return None
    for restaurant in restaurants:
        restaurants_id_list.append(restaurant.id)
    restaurants_id_list = set(restaurants_id_list)
    return restaurants_id_list


def get_restaurants_id_address(address):
    """
        작성자 : 서재환
    """
    restaurants_id_list = []
    address_queryset = Restaurant.objects.filter(address__contains = address)
    
    if len(address_queryset) == 0:
        return None
    for restaurant in address_queryset:
        restaurants_id_list.append(restaurant.id)
    restaurants_id_list = set(restaurants_id_list)
    return restaurants_id_list


def is_res_in_pos(group_name):
    """
    editor: 서재환
    """
    restaurants_id_list = get_restaurants_id(group_name)
    arr = []
    for id in restaurants_id_list:
        restaurant = Restaurant.objects.get(id=id)
        if restaurant:
            arr.append(restaurant.id)
    if len(arr) == 0:
        return False
    return True


def date_return_cons(request):
    """
    editor: 서재환
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    q = Q()

    if start_date == None and end_date == None:
        return q
    elif start_date != None and end_date == None:
        q.add(Q(timestamp = start_date), q.AND)
    elif start_date == None and end_date != None:
        q.add(Q(timestamp = end_date), q.AND)
    elif start_date > end_date:
        return
    elif start_date is not None and end_date is not None:
        q.add(Q(timestamp__range = (start_date, end_date)), q.AND)
    return q


def is_timeunit(request):
    """
    editor: 서재환
    """
    timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
    timeunit = request.GET.get('timeunit')
    if timeunit not in timeunit_group:
        return False
    return True


def fake_deserializer_year(queryset):
    """
    editor: 서재환
    """
    res = []
    price_arr = []
    timestamp_arr = []
    price_start = 0
    if len(queryset) == 0:
        return []
    start_year = str(queryset[0]['year'])
    for date_info in queryset:
        date = str(date_info['timestamp']).split('-')[0]
        year = str(date.split('-')[0])
        price = date_info['total_price']
        timestamp_arr.append(date)
        if year == start_year:
            price_start += price
        else:
            price_arr.append(price_start)
            start_year = year
            price_start = 0
            price_start += price
    if price_start != 0:
        price_arr.append(price_start)
    timestamp_arr = sorted(set(timestamp_arr))
    for i in range(len(timestamp_arr)):
        res.append({'timestamp': timestamp_arr[i], 'total_price': price_arr[i]})
    return res


def put_zero(str):
    """
    editor: 서재환
    """
    if len(str) == 1:
        str = '0' + str
    return str


def fake_desrializer_month(queryset):
    """
    editor: 서재환
    """
    res = []
    price_arr = []
    timestamp_arr = []
    price_start = 0
    if len(queryset) == 0:
        return []
    start_month = put_zero(str(queryset[0]['month']))
    for date_info in queryset:
        date = str(date_info['timestamp']).split(' ')[0]
        date = date.split('-')[0] + '-' + date.split('-')[1]
        month = str(date.split('-')[1])
        price = date_info['total_price']
        timestamp_arr.append(date)
        print(month, start_month)
        if month == start_month:
            price_start += price
        else:
            price_arr.append(price_start)
            start_month = month
            price_start = 0
            price_start += price
    if price_start != 0:
        price_arr.append(price_start)
    timestamp_arr = sorted(set(timestamp_arr))
    for i in range(len(timestamp_arr)):
        res.append({'timestamp': timestamp_arr[i], 'total_price': price_arr[i]})
    return res


def fake_deserializer_week(queryset):
    """
    editor: 서재환
    """
    res = []
    price_arr = []
    week_arr = []
    price_start = 0
    if len(queryset) == 0:
        return []
    start_week = str(queryset[0]['week'])
    for date_info in queryset:
        price = date_info['total_price']
        week = str(date_info['week'])
        if week == start_week:
            price_start += price
        else:
            price_arr.append(price_start)
            week_arr.append(start_week)
            start_week = week
            price_start = 0
            price_start += price

    if price_start != 0:
        price_arr.append(price_start)
    if start_week  != 0:
        week_arr.append(start_week)
    print(week_arr, price_arr)
    for i in range(len(price_arr)):
        res.append({'week': week_arr[i], 'total_price': price_arr[i]})
    return res


def fake_deserializer_day(queryset):
    """
    editor: 서재환
    """
    res = []
    price_arr = []
    timestamp_arr = []
    price_start = 0
    if len(queryset) == 0:
        return []
    start_day = str(queryset[0]['day'])
    for date_info in queryset:
        date = str(date_info['timestamp']).split(' ')[0]
        day = str(date.split('-')[2])
        price = date_info['total_price']
        timestamp_arr.append(date)
        if day == start_day:
            price_start += price
        else:
            price_arr.append(price_start)
            start_day = day
            price_start = 0
            price_start += price
    if price_start != 0:
        price_arr.append(price_start)
    timestamp_arr = sorted(set(timestamp_arr))
    for i in range(len(timestamp_arr)):
        res.append({'timestamp': timestamp_arr[i], 'total_price': price_arr[i]})
    return res


def fake_deserializer_hour(queryset):
    """
    editor: 서재환
    """
    res = []
    price_arr = []
    timestamp_arr = []
    price_start = 0
    if len(queryset) == 0:
        return []
    start_hour = str(queryset[0]['hour'])
    for date_info in queryset:
        date = str(date_info['timestamp']).split(' ')[0] + ' '
        hour = str(date_info['timestamp']).split(' ')[1].split(':')[0]
        date = date + hour
        price = date_info['total_price']
        timestamp_arr.append(date)
        if start_hour == hour:
            price_start += price
        else:
            price_arr.append(price_start)
            start_hour = hour
            price_start = 0
            price_start += price
    if price_start != 0:
        price_arr.append(price_start)
    if start_hour  != 0:
        timestamp_arr.append(start_hour)
    timestamp_arr = sorted(set(timestamp_arr))
    for i in range(len(timestamp_arr)):
        res.append({'timestamp': timestamp_arr[i], 'total_price': price_arr[i]})
    return res


def timeunit_return_queryset(request, guests):
    """
    editor: 서재환
    """
    timeunit = request.GET.get('timeunit')
    timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
    if timeunit:
        timeunit = timeunit.upper()
    if timeunit and timeunit in timeunit_group:
        if timeunit == 'YEAR':
            guests = guests.values('timestamp') \
                .annotate(year=ExtractYear('timestamp'), total_price=Sum('price'))
            guests = guests.values('timestamp','total_price','year')
            guests = fake_deserializer_year(guests)        
        elif timeunit == 'MONTH':
            guests = guests.values('timestamp') \
                .annotate(month=ExtractMonth('timestamp'), total_price=Sum('price'))
            guests = guests.values('timestamp','total_price','month')
            guests = fake_desrializer_month(guests)
        elif timeunit == 'WEEK':
            guests = guests.values('timestamp') \
                .annotate(week=ExtractWeek('timestamp'), total_price=Sum('price'))
            guests = guests.values('timestamp','total_price','week')
            guests = fake_deserializer_week(guests)                
        elif timeunit == 'DAY':
            guests = guests.values('timestamp') \
                .annotate(day=ExtractDay('timestamp'), total_price=Sum('price'))
            guests = guests.values('timestamp', 'total_price', 'day')
            guests = fake_deserializer_day(guests)
        elif timeunit == 'HOUR':
            guests = guests.values('timestamp') \
                .annotate(hour=ExtractHour('timestamp'), total_price=Sum('price'))
        return guests

    return Response({'error_message': "['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR'] 중 하나의 인자 값을 넣으시오"})


def is_city_exsist(city_name):
    queryset = Restaurant.objects.filter(address__contains=city_name)
    if len(queryset) == 0:
        return False
    return True