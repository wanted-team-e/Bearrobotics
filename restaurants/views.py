from inspect import Parameter
from msilib import type_string
from django.db.models import Q, Sum, Count, F
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractDay, ExtractHour
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from restaurants.models import Restaurant, Guest, Group
from restaurants.serializers import RestaurantCUDSerializer, RestaurantRSerializer, TotalPriceDocsSerializer, PaymentDocsSerializer, PartyDocsSerializer, GuestSerializer, GroupSerializer    

from restaurants.utils import commons


class RestaurantViewset(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantCUDSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RestaurantRSerializer
        elif self.action == 'total_price' or self.action == 'total_price_restaurant':
            return TotalPriceDocsSerializer
        elif self.action == 'payment' or self.action == 'payment_restaurant':
            return PaymentDocsSerializer
        elif self.action == 'party' or self.action == 'party_restaurant':
            return PartyDocsSerializer
        else:
            return RestaurantCUDSerializer

    @swagger_auto_schema(
        operation_description='POST /api/restaurant',
        operation_summary='Return Fields: (name, city, address, group)'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='PUT /api/restaurant/:pk',
        operation_summary='Return Fields: (name, city, address, group)'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='DELETE /api/restaurant',
        operation_summary='Return Fields: (name, city, address, group)'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='GET /api/restaurant',
        operation_summary='Return Fields: (name, city, address, group_name)'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='GET /api/restaurant/:pk',
        operation_summary='Return Fields: (name, city, address, group_name)'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



    @swagger_auto_schema(
        operation_description='GET /api/restaurant/total_price',
        operation_summary='Return Fields: (timeunit, restaurant_id, total_price)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=False, methods=['get'])
    def total_price(self, request):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

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

    @swagger_auto_schema(
        operation_description='GET /api/restaurant/payment',
        operation_summary='Return Fields: (timeunit, restaurant_id, payment, count)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=False, methods=['get'])
    def payment(self, request):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

        if exception_chk.get('occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query')

            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').upper()
            timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

            if timeunit and timeunit in timeunit_group:
                if timeunit == 'YEAR':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(year=ExtractYear('timestamp'), count=Count('payment'))
                elif timeunit == 'MONTH':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(month=ExtractMonth('timestamp'), count=Count('payment'))
                elif timeunit == 'WEEK':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(week=ExtractWeek('timestamp'), count=Count('payment'))
                elif timeunit == 'DAY':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(day=ExtractDay('timestamp'), count=Count('payment'))
                elif timeunit == 'HOUR':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(hour=ExtractHour('timestamp'), count=Count('payment'))

                return Response(guests, status=status.HTTP_200_OK)
            else:
                return Response({'error_message': "시간 단위는 &timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(
        operation_description='GET /api/restaurant/party',
        operation_summary='Return Fields: (timeunit, resturant_id, number_of_party, count)',
        manual_parameters=commons.set_swagger()
        )
    @action(detail=False, methods=['get'])
    def party(self, request):

        """
            작성자: 김채욱
        """

        exception_chk = commons.exception_handling(request)

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
                        .annotate(year=ExtractYear('timestamp'), restaurant_id=F('restaurant'),
                                  count=Count('number_of_party'))
                elif timeunit == 'MONTH':
                    guests = guests.values('number_of_party') \
                        .annotate(month=ExtractMonth('timestamp'), restaurant_id=F('restaurant'),
                                  count=Count('number_of_party'))
                elif timeunit == 'WEEK':
                    guests = guests.values('number_of_party') \
                        .annotate(week=ExtractWeek('timestamp'), restaurant_id=F('restaurant'),
                                  count=Count('number_of_party'))
                elif timeunit == 'DAY':
                    guests = guests.values('number_of_party') \
                        .annotate(day=ExtractDay('timestamp'), restaurant_id=F('restaurant'),
                                  count=Count('number_of_party'))
                elif timeunit == 'HOUR':
                    guests = guests.values('number_of_party') \
                        .annotate(hour=ExtractHour('timestamp'), restaurant_id=F('restaurant'),
                                  count=Count('number_of_party'))

                return Response(guests, status=status.HTTP_200_OK)
            else:
                return Response({'error_message': "시간 단위는 &timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(
        operation_description='GET /api/restaurant/:pk/total_price_restaurant',
        operation_summary='Return Fields: (timeunit, restaurant_id, total_price)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=True, methods=['get'])
    def total_price_restaurant(self, request, pk):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

        if exception_chk.get('occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query') & Q(restaurant__id=pk)

            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').upper()
            timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

            if timeunit and timeunit in timeunit_group:
                if timeunit == 'YEAR':
                    guests = guests.values('restaurant_id')\
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

    @swagger_auto_schema(
        operation_description='GET /api/restaurant/:pk/payment_restaurant',
        operation_summary='Return Fields: (timeunit, restaurant_id, payment, count)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=True, methods=['get'])
    def payment_restaurant(self, request, pk):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

        if exception_chk.get('occurred'):
            return exception_chk.get('error')

        try:
            print('try진입')
            query = exception_chk.get('query') & Q(restaurant__id=pk)

            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').upper()
            timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

            if timeunit and timeunit in timeunit_group:
                if timeunit == 'YEAR':
                    print('year진입')
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(year=ExtractYear('timestamp'), count=Count('payment'))
                    print(guests.query)
                elif timeunit == 'MONTH':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(month=ExtractMonth('timestamp'), count=Count('payment'))
                elif timeunit == 'WEEK':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(week=ExtractWeek('timestamp'), count=Count('payment'))
                elif timeunit == 'DAY':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(day=ExtractDay('timestamp'), count=Count('payment'))
                elif timeunit == 'HOUR':
                    guests = guests.values('restaurant_id', 'payment') \
                        .annotate(hour=ExtractHour('timestamp'), count=Count('payment'))

                return Response(guests, status=status.HTTP_200_OK)
            else:
                return Response({'error_message': "시간 단위는 &timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                            "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(
        operation_description='GET /api/restaurant/:pk/party_restaurant',
        operation_summary='Return Fields: (timeunit, resturant_id, number_of_party, count)',
        manual_parameters=commons.set_swagger()
        )
    @action(detail=True, methods=['get'])
    def party_restaurant(self, request, pk):

        """
            작성자: 김채욱
        """

        exception_chk = commons.exception_handling(request)

        if exception_chk.get('occurred'):
            return exception_chk.get('error')

        try:

            query = exception_chk.get('query') & Q(restaurant__id=pk)

            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').upper()
            timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

            if timeunit and timeunit in timeunit_group:
                if timeunit == 'YEAR':
                    guests = guests.values('number_of_party') \
                        .annotate(year=ExtractYear('timestamp'), count=Count('number_of_party'))
                                  
                elif timeunit == 'MONTH':
                    guests = guests.values('number_of_party') \
                        .annotate(month=ExtractMonth('timestamp'), count=Count('number_of_party'))
                elif timeunit == 'WEEK':
                    guests = guests.values('number_of_party') \
                        .annotate(week=ExtractWeek('timestamp'), count=Count('number_of_party'))
                elif timeunit == 'DAY':
                    guests = guests.values('number_of_party') \
                        .annotate(day=ExtractDay('timestamp'), count=Count('number_of_party'))
                elif timeunit == 'HOUR':
                    guests = guests.values('number_of_party') \
                        .annotate(hour=ExtractHour('timestamp'), count=Count('number_of_party'))

                return Response(guests, status=status.HTTP_200_OK)
            else:
                return Response({'error_message': "시간 단위는 &timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view

class GuestViewset(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

"""
    editor: 서재환
"""
@api_view(['GET'])
def get_guest(request):
    group_list = Guest.objects.all()
    serializer = GuestSerializer(group_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_certain_group_list(request, group_name):
    restaurants_id_list = []
    certain_group = []

    requests = commons._request_param(request)    
    print(f'*****requests***** {requests}{group_name}')

    """
    그룹 이름이 그룹 테이블에 있는지 확인
    있으면 그룹 아이디 추출
    """
    try:
        group = Group.objects.get(name = group_name)
        id = group.id
    except: 
        return Response({'error_message': '해당 그룹이 없습니다.'})
    
    """
    그룹 이름에 해당하는 아이디가 레스토랑 테이블엥 있는지 확인
    있으면 레스토랑 아이디 추출 후 제약조건 추가
    """

    restaurants = Restaurant.objects.filter(group_id=id)
    if len(restaurants) == 0:
        return Response({'error_message': '해당 그룹에 해당하는 레스토랑이 없습니다.'})
    for restaurant in restaurants:
        restaurants_id_list.append(restaurant.id)
    restaurants_id_list = set(restaurants_id_list)

    q2 = Q()
    for id in restaurants_id_list:
        q2.add(Q(restaurant_id = id), q2.OR)

    """
    파라미터로 기간을 조회 시 시작과 끝 값이 있거나 없을 때 총 4가지 경우 처리
    시작과 끝 날짜가 없을 때 그룹이름에 해당하는 POS 데이터가 모두 출력되게 함
    """

    if requests.get('start_time') == None and requests.get('end_time') == None:
        certain_group += Guest.objects.filter(q2)
        if len(certain_group) == 0:
            return Response({'error_message': '해당 그룹에 해당하는 레스토랑 결제 내역이 없습니다.'})
        serializer = GuestSerializer(certain_group, many=True)
        return Response(serializer.data)
    
    if requests['start_time'] != None and requests['end_time'] != None:
        q2.add(Q(timestamp__range=(requests.get('start_time'), requests['end_time'])), q2.AND)
        q2 &= q2
    elif not (requests['start_time'] == None and requests['end_time'] == None):
        if requests['start_time'] == None:
            q2.add(Q(timestamp = requests['end_time']), q2.AND)
        elif requests['start_time'] != None:
            q2.add(Q(timestamp = requests['start_time']), q2.AND)
        q2 &= q2            
    
    guests = Guest.objects.filter(q2).order_by('timestamp')

    """
    파라미터 timeunit에 대한 처리
    """
    timeunit = requests.get('timeunit')
    print(f'timeunit: {timeunit}')
    timeunit_list = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
    if not timeunit and timeunit in timeunit_list:
        return Response({'error_message': "파라미터 timeunit 값을 'HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR' 중 하나를 넣어주세요."})
    if timeunit == 'DAY':
        guests = Guest.objects.values() \
            .annotate(day=ExtractDay('timestamp'), total_price = Sum('price'))
    certain_group += guests
    serializer = GuestSerializer(certain_group, many=True)
    return Response(serializer.data)

    # if timeunit and timeunit in timeunit_group:
    # if timeunit == 'YEAR':
    #     guests = guests.values('restaurant_id') \
    #         .annotate(year=ExtractYear('timestamp'), total_price=Sum('price'))
    # elif timeunit == 'MONTH':
    #     guests = guests.values('restaurant_id') \
    #         .annotate(month=ExtractMonth('timestamp'), total_price=Sum('price'))
    # elif timeunit == 'WEEK':
    #     guests = guests.values('restaurant_id') \
    #         .annotate(week=ExtractWeek('timestamp'), total_price=Sum('price'))
    # elif timeunit == 'DAY':
    #     guests = guests.values('restaurant_id') \
    #         .annotate(day=ExtractDay('timestamp'), total_price=Sum('price'))
    # elif timeunit == 'HOUR':
    #     guests = guests.values('restaurant_id') \
    #         .annotate(hour=ExtractHour('timestamp'), total_price=Sum('price'))