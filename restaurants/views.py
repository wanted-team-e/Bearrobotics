from django.db.models import Q, Min, Max, Sum
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractDay, ExtractHour
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from restaurants.models import Restaurant, Guest
from restaurants.serializers import RestaurantSerializer


class RestaurantViewset(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=False, methods=['get'])
    def total_price(self, request):
        """
            editor : 강정희
        """
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        timeunit = request.query_params.get('timeunit', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        min_party = request.query_params.get('min_party', None)
        max_party = request.query_params.get('max_party', None)
        group = request.query_params.get('group', None)

        # request 입력값에 대한 예외처리
        if start_time > end_time:
            return Response({'error_message': "조회 시작 날짜보다 끝 날짜가 빠를 수 없습니다."},
                            status=status.HTTP_400_BAD_REQUEST)
        if min_price and max_price and min_price > max_price:
            print(min_price.isdigit())
            return Response({'error_message': "조회 시작 날짜보다 끝 날짜가 빠를 수 없습니다."},
                            status=status.HTTP_400_BAD_REQUEST)
        # if min_party > max_party:
        #     return Response({'error_message': "조회 시작 날짜보다 끝 날짜가 빠를 수 없습니다."},
        #                     status=status.HTTP_400_BAD_REQUEST)

        try:
            query = Q(timestamp__range=(start_time, end_time))

            if min_price and max_price:
                query &= Q(price__range=(min_price, max_price))
            if min_party and max_party:
                query &= Q(number_of_party__range=(min_party, max_party))
            if group:
                query &= Q(restaurant__group__name=group)

            guests = Guest.objects.filter(query)

            timeunit = timeunit.upper()
            timeunit_group = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
            print(timeunit)
            print(timeunit and timeunit in timeunit_group)

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
            print('first try-except')
            print(e)
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)
