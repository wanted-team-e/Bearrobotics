from datetime import datetime
from django.db.models import Q
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractDay, ExtractHour
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from restaurants.models import Guest


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

    is_error_occurred = False
    error = ''

    # base query 작성
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
                is_error_occurred = True
                error = Response({'error_message': "조회 시작 날짜보다 끝 날짜가 빠를 수 없습니다."},
                                 status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            is_error_occurred = True
            error = Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                               "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    if requests.get('min_price') and requests.get('max_price'):
        if not (requests.get('min_price').isdigit() or requests.get('max_price').isdigit()):
            is_error_occurred = True
            error = Response({'error_message': "조회 최소 가격, 최대 가격은 숫자값을 입력해야합니다."},
                             status=status.HTTP_400_BAD_REQUEST)
        if requests.get('min_price') > requests.get('max_price'):
            is_error_occurred = True
            error = Response({'error_message': "조회 최소 가격보다 최대 가격이 클 수 없습니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    if requests.get('min_party') and requests.get('max_party'):
        if requests.get('min_party').isdigit() or requests.get('max_party').isdigit():
            is_error_occurred = True
            error = Response({'error_message': "조회 최소 방문자 수, 최대 방문자 수는 숫자값을 입력해야합니다."},
                             status=status.HTTP_400_BAD_REQUEST)
        if requests.get('min_party') > requests.get('max_party'):
            is_error_occurred = True
            error = Response({'error_message': "조회 최소 방문자 수보다 최대 방문자 수가 클 수 없습니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    if requests.get('group'):
        group_chk = Guest.objects.filter(query).exists()

        if not group_chk:
            is_error_occurred = True
            error = Response({'error_message': "조회 그룹 이름이 존재하지 않습니다."},
                             status=status.HTTP_400_BAD_REQUEST)

    result = {
        'timeunit': requests.get('timeunit'),
        'query': query,
        'is_error_occurred': is_error_occurred,
        'error': error
    }
    return result


def set_extract_time(timeunit):
    """
        작성자 : 강정희
    """
    # timeunit에 따른 annotate 함수 설정
    timeunit_group = ['year', 'month', 'week', 'day', 'hour']

    extract_time_dict = {
        'year': ExtractYear('timestamp'),
        'month': ExtractMonth('timestamp'),
        'week': ExtractWeek('timestamp'),
        'day': ExtractDay('timestamp'),
        'hour': ExtractHour('timestamp'),
    }

    if timeunit in timeunit_group:
        return extract_time_dict[timeunit]
    else:
        raise Exception


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
