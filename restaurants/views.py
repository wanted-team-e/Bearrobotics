from datetime import datetime
from django.db.models import Q, Sum, Count
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractDay, ExtractHour
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from restaurants.models import Restaurant, Guest
from restaurants.serializers import RestaurantSerializer, TotalPriceDocsSerializer


def _request_param(request):
    """
        editor : 강정희
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


def _exception_handling(request):
    """
        editor : 강정희
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
            date_format = "%Y-%m-%d %H:%M:%S"
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
        if requests.get('min_price').isdigit() or requests.get('max_price').isdigit():
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


class RestaurantViewset(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_class(self):
        if self.action == 'total_price':
            return TotalPriceDocsSerializer
        else:
            return RestaurantSerializer


    @swagger_auto_schema(operation_summary='create뷰입니다.')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='update뷰입니다.')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary='전체 가격 반환 api입니다.')
    @action(detail=False, methods=['get'])
    def total_price(self, request):
        """
            editor : 강정희

        """
        exception_chk = _exception_handling(request)

        if exception_chk.get('occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query')

            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').upper()
            timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

            if timeunit and timeunit in timeunit_group:
                if timeunit == 'YEAR':
                    guests = guests.values('restaurant_id') \
                        .annotate(year=ExtractYear('timestamp'), total_price=Sum('price'))
                elif timeunit == 'MONTH':
                    guests = guests.values('restaurant_id') \
                        .annotate(month=ExtractMonth('timestamp'), total_price=Sum('price'))
                elif timeunit == 'WEEK':
                    guests = guests.values('restaurant_id') \
                        .annotate(week=ExtractWeek('timestamp'), total_price=Sum('price'))
                elif timeunit == 'DAY':
                    guests = guests.values('restaurant_id') \
                        .annotate(day=ExtractDay('timestamp'), total_price=Sum('price'))
                elif timeunit == 'HOUR':
                    guests = guests.values('restaurant_id') \
                        .annotate(hour=ExtractHour('timestamp'), total_price=Sum('price'))

                return Response(guests, status=status.HTTP_200_OK)
            else:
                return Response({'error_message': "시간 단위는 &timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def payment(self, request):
        pass

    @action(detail=False, methods=['get'])
    def party(self, request):

        """
            작성자: 김채욱
        """

        exception_chk = _exception_handling(request)

        if exception_chk.get('occurred'):
            return exception_chk.get('error')

        try:

            query = exception_chk.get('query')

            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').upper()
            timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

            if timeunit and timeunit in timeunit_group:
                if timeunit == 'YEAR':
                    guests = guests.values('number_of_party') \
                        .annotate(year=ExtractYear('timestamp'),restaurant_id=F('restaurant'), count=Count('number_of_party'))
                elif timeunit == 'MONTH':
                    guests = guests.values('number_of_party') \
                        .annotate(month=ExtractMonth('timestamp'),restaurant_id=F('restaurant'), count=Count('number_of_party'))
                elif timeunit == 'WEEK':
                    guests = guests.values('number_of_party') \
                        .annotate(week=ExtractWeek('timestamp'),restaurant_id=F('restaurant'), count=Count('number_of_party')) 
                elif timeunit == 'DAY':
                    guests = guests.values('number_of_party') \
                        .annotate(day=ExtractDay('timestamp'),restaurant_id=F('restaurant'), count=Count('number_of_party'))
                elif timeunit == 'HOUR':
                    guests = guests.values('number_of_party') \
                        .annotate(hour=ExtractHour('timestamp'),restaurant_id=F('restaurant'), count=Count('number_of_party'))

                return Response(guests, status=status.HTTP_200_OK)
            else:
                return Response({'error_message': "시간 단위는 &timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)