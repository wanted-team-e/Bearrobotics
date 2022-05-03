from django.db.models import Q, Min, Max
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

        if start_time and end_time and timeunit:
            try:

                # if not min_price: min_price = Guest.objects.aggrgate(Min('price'))['price_min']
                # if not max_price: max_price = Guest.objects.aggrgate(Max('price'))['price_max']
                # if not min_party: max_price = Guest.objects.aggrgate(Min('number_of_party'))['number_of_party_min']
                # if not max_party: max_price = Guest.objects.aggrgate(Max('number_of_party'))['number_of_party_max']

                query = Q(timestamp__range=(start_time, end_time))

                if min_price and max_price:
                    query &= Q(price__range=(min_price, max_price))
                if min_party and max_party:
                    query &= Q(number_of_party__range=(min_party, max_party))
                if group:
                    query &= Q(restaurant__group__id=group)

                guests = Guest.objects.filter(query)
            except Exception as e:
                print(e)
                return Response({'error_message': "기간은 'start_time=yyyy-mm-dd&end_time=yyyy-mm-dd"
                                                  "&timeunit=hour/day/week/month/year' 형식으로 요청 가능합니다."},
                                status=status.HTTP_400_BAD_REQUEST)



        return Response(results, status=status.HTTP_200_OK)
