from django.db.models import Sum, Count, F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from restaurants.models import Guest
from restaurants.serializers import GuestCUDSerializer, GuestRSerializer, TotalPriceDocsSerializer, PaymentDocsSerializer, PartyDocsSerializer

from restaurants.utils import commons


class GuestViewset(viewsets.ModelViewSet):
    """
        작성자 : 서재환
    """
    queryset = Guest.objects.all()
    serializer_class = GuestCUDSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return GuestRSerializer
        elif self.action == 'total_price':
            return TotalPriceDocsSerializer
        elif self.action == 'payment':
            return PaymentDocsSerializer
        elif self.action == 'party':
            return PartyDocsSerializer
        else:
            return GuestCUDSerializer

    @swagger_auto_schema(
        operation_description='POST /api/pos',
        operation_summary='Return Fields: (restaurant, price, number_of_party, timestamp, payment)'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='PUT /api/pos/:pk',
        operation_summary='Return Fields: (restaurant, price, number_of_party, timestamp, payment)'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='DELETE /api/pos',
        operation_summary='Return Fields: (restaurant, price, number_of_party, timestamp, payment)'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='GET /api/pos',
        operation_summary='Return Fields: (restaurant_name, price, number_of_party, timestamp, payment)'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='GET /api/pos/:pk',
        operation_summary='Return Fields: (restaurant_name, price, number_of_party, timestamp, payment)'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='GET /api/pos/total_price',
        operation_summary='Return Fields: (timeunit, restaurant_id, total_price)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=False, methods=['get'])
    def total_price(self, request):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

        if exception_chk.get('is_error_occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query')
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
        except Exception as e:
            return Response({'error_message': "기간은 'start_time=yyyy-mm-dd 00:00:00&end_time=yyyy-mm-dd 00:00:00"
                                              "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='GET /api/pos/payment',
        operation_summary='Return Fields: (timeunit, restaurant_id, payment, count)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=False, methods=['get'])
    def payment(self, request):
        """
            작성자 : 강정희
        """
        exception_chk = commons.exception_handling(request)

        if exception_chk.get('is_error_occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query')
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
        operation_description='GET /api/pos/party',
        operation_summary='Return Fields: (timeunit, restaurant_id, number_of_party, count)',
        manual_parameters=commons.set_swagger()
    )
    @action(detail=False, methods=['get'])
    def party(self, request):

        """
            작성자: 김채욱
        """

        exception_chk = commons.exception_handling(request)

        if exception_chk.get('is_error_occurred'):
            return exception_chk.get('error')

        try:
            query = exception_chk.get('query')
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