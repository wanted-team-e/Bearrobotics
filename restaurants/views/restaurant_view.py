from django.db.models import Q, Sum, Count, F
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from restaurants.models import Restaurant, Guest
from restaurants.permissions import RestaurantPermission
from restaurants.serializers import RestaurantCUDSerializer, RestaurantRSerializer, \
    TotalPriceDocsSerializer, PaymentDocsSerializer, PartyDocsSerializer, GuestCUDSerializer

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
    def total_price(self, request, pk):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

        if exception_chk.get('is_error_occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query') & Q(restaurant__id=pk)
            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').lower()

            if timeunit:
                annotate_options = {
                    timeunit.lower(): commons.set_extract_time(timeunit),
                    'total_price': Sum('price')
                }

                guests = guests.values('restaurant_id').annotate(**annotate_options)
                print(guests.query)

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
    def payment(self, request, pk):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

        if exception_chk.get('is_error_occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query') & Q(restaurant__id=pk)
            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').lower()

            if timeunit:
                annotate_options = {
                    timeunit.lower(): commons.set_extract_time(timeunit),
                    'restaurant_id': F('restaurant'),
                    'count': Count('payment')
                }

                guests = guests.values('payment').annotate(**annotate_options)

                return Response(guests, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='GET /api/restaurant/:pk/party',
        operation_summary='Return Fields: (timeunit, restaurant_id, number_of_party, count)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=True, methods=['get'])
    def party(self, request, pk):

        """
            작성자: 김채욱
        """

        exception_chk = commons.exception_handling(request)

        if exception_chk.get('is_error_occurred'):
            return exception_chk.get('error')

        try:

            query = exception_chk.get('query') & Q(restaurant__id=pk)
            guests = Guest.objects.filter(query)

            timeunit = exception_chk.get('timeunit').lower()

            if timeunit:
                annotate_options = {
                    timeunit.lower(): commons.set_extract_time(timeunit),
                    'restaurant_id': F('restaurant'),
                    'count': Count('number_of_party')
                }

                guests = guests.values('number_of_party').annotate(**annotate_options)

                return Response(guests, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)


from restaurants.utils.commons import *


@swagger_auto_schema(
    method='get',
    operation_description='GET api/pos/',
    operation_summary='Return Fields: (restaurant_name, price, number_of_party, timestamp, payment)',
)

@api_view(['GET'])
def get_guest(self):
    """
        작성자 : 서재환
    """
    group_list = Guest.objects.all()
    serializer = GuestCUDSerializer(group_list, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    operation_description='GET api/group/',
    operation_summary='Return Fields: (restaurant_id, price, number_of_party, timestamp, payment)',
)

@api_view(['GET'])
def get_certain_group_list(request, group_name):
    """
        작성자 : 서재환
    """
    q = Q()
    guests = []
    if group_name and not is_group_name_in_group(group_name):
        return Response({'error_message': '해당 그룹이 없습니다.'})
    if get_restaurants_id(group_name) == None:
        return Response({'error_message': '그룹이름에 해당하는 레스토랑이 없습니다.'})
    if group_name and not is_res_in_pos(group_name):
        return Response({'error_message': '레스토랑이 POS기에 없습니다.'})
    if not isinstance(date_return_cons(request), Q):
        return Response({'error_message': 'start_date가 end_date 보다 작아야됩니다.'})
    restaurants_id = get_restaurants_id(group_name)
    for id in restaurants_id:
        guests += Guest.objects.filter(restaurant_id = id)
    q = q.add(date_return_cons(request), q.AND)
    if not request.GET.get('timeunit') and not request.GET.get('start_date') and not request.GET.get('end_date'):
        serializer = GuestCUDSerializer(guests, many=True)
        return Response(serializer.data)
    if request.GET.get('timeunit') and not is_timeunit(request):
        return Response({'error_message': "timeunit은 ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']중 하나"})
    if isinstance(date_return_cons(request), Q) and not request.GET.get('timeunit'):
        guest = Guest.objects.none()
        for id in restaurants_id:
            query_set = Guest.objects.filter(restaurant_id = id)
            guest |= query_set
        guests = guest.filter(q).order_by('timestamp')
        serializer = GuestCUDSerializer(guests, many=True)
        return Response(serializer.data)
    if request.GET.get('timeunit') and is_timeunit(request):
        guests = Guest.objects.filter(q)
        queryset = timeunit_return_queryset(request, guests)
        return Response(queryset)


@swagger_auto_schema(
    method='get',
    operation_description='GET api/address/',
    operation_summary='Return Fields: (restaurant_id, price, number_of_party, timestamp, payment)',
)

@api_view(['GET'])
def get_city_list(request, city_name):
    """
        작성자 : 서재환
    """
    q = Q()
    restaurant_id_list = []

    if not is_city_exsist:
        return Response({'error_message': '입력하신 도시에 레스토랑이 없습니다.'})
    if is_city_exsist and not request.GET.get('start_date') and not request.GET.get('end_date') and not request.GET.get('timeunit'):
        queryset = Restaurant.objects.filter(address__contains=city_name)
        for restaurant in queryset:
            restaurant_id_list.append(restaurant.id)
        guests = Guest.objects.none()
        for id in restaurant_id_list:
            guest = Guest.objects.filter(restaurant_id=id)
            guests |= guest
        guests = guests.order_by('timestamp')
        if len(guests) == 0:
            return Response({'error_message': 'pos에 해당 도시에 있는 레스토랑이 없습니다.'})
        guests = GuestCUDSerializer(guests, many=True)
        return Response(guests.data)
    restaurant_id_list = get_restaurants_id_address(city_name)
    if not isinstance(date_return_cons(request), Q):
        return Response({'error_message': 'start_date가 end_date 보다 작아야됩니다.'})
    if request.GET.get('timeunit') and not is_timeunit(request):
        return Response({'error_message': "timeunit은 ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']중 하나"})
    if isinstance(date_return_cons(request), Q) and not request.GET.get('timeunit'):
        q &= date_return_cons(request)
        guest = Guest.objects.none()
        for id in restaurant_id_list:
            query_set = Guest.objects.filter(restaurant_id = id)
            guest |= query_set
        guests = guest.filter(q).order_by('timestamp')
        serializer = GuestCUDSerializer(guests, many=True)
        return Response(serializer.data)
    if request.GET.get('timeunit') and is_timeunit(request):
        q &= date_return_cons(request)
        guest = Guest.objects.none()
        for id in restaurant_id_list:
            query_set = Guest.objects.filter(restaurant_id = id)
            guest |= query_set
        guests = guest.filter(q).order_by('timestamp')
        queryset = timeunit_return_queryset(request, guests)
        return Response(queryset)
