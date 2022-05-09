from django.db.models import Q, Sum, Count, F
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractDay, ExtractHour
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from restaurants.models import Restaurant, Guest, Group
from restaurants.permissions import RestaurantPermission
from restaurants.serializers import RestaurantCUDSerializer, RestaurantRSerializer, TotalPriceDocsSerializer, PaymentDocsSerializer, PartyDocsSerializer, GuestCUDSerializer

from restaurants.utils import commons


class RestaurantViewset(viewsets.ModelViewSet):
    """
        작성자 : 강정희
    """
    queryset = Restaurant.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [RestaurantPermission]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RestaurantRSerializer
        elif self.action == 'total_price':
            return TotalPriceDocsSerializer
        elif self.action == 'payment':
            return PaymentDocsSerializer
        elif self.action == 'party':
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
        operation_description='GET /api/restaurant/:pk/total_price',
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
        operation_description='GET /api/restaurant/:pk/payment',
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
        operation_description='GET /api/restaurant/:pk/party',
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


@api_view(['GET'])
def get_guest(self):
    """
        작성자 : 서재환
    """
    group_list = Guest.objects.all()
    serializer = GuestCUDSerializer(group_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_certain_group_list(self, request):
    """
        작성자 : 서재환
    """
    restaurants_id_list = []
    group_name = request.GET.get('group_name', False)

    if not group_name:
        return Response({'error_message': '인자 값으로 그룹 이름을 넣어주세요.'}, stats=status.HTTP_400_BAD_REQUEST)
    
    groups = Group.objects.all().filter(name=group_name)

    if len(groups) == 0:
        return Response({'error_message': '해당 그룹이 없습니다.'}, stats=status.HTTP_400_BAD_REQUEST)

    group_id = groups[0].id 
    
    restaurants = Restaurant.objects.all().filter(group_id==group_id)

    if len(restaurants) == 0:
        return Response({'error_message': '해당 그룹에 해당하는 레스토랑이 없습니다.'}, stats=status.HTTP_400_BAD_REQUEST)

    for id in restaurants:
        restaurants_id_list.append(restaurants[id])
    restaurants_id_list = set(restaurants_id_list)

    for id in restaurants_id_list:
        certain_group = Guest.objects.all().filter(restaurnat_id = id)

    serializer = GuestCUDSerializer(certain_group, many=True)
    return Response(serializer.data)
