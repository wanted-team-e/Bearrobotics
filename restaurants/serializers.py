from rest_framework import serializers

from restaurants.models import Restaurant, Guest


class RestaurantCUDSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    class Meta:
        model = Restaurant
        fields = (
            'name',
            'city',
            'address',
            'group',
        )


class RestaurantRSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Restaurant
        fields = (
            'name',
            'city',
            'address',
            'group_name',
        )


class TotalPriceDocsSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    timeunit = serializers.CharField()
    total_price = serializers.IntegerField()

    class Meta:
        model = Guest
        fields = (
            'timeunit',
            'restaurant',
            'total_price',
        )


class PaymentDocsSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    timeunit = serializers.CharField()
    count = serializers.IntegerField()

    class Meta:
        model = Guest
        fields = (
            'timeunit',
            'restaurant',
            'payment',
            'count',
        )

class PartyDocsSerializer(serializers.ModelSerializer):
    """
        작성자 : 김채욱
    """
    timeunit = serializers.CharField()
    count = serializers.IntegerField()
    restaurant_id = serializers.IntegerField()
    
    class Meta:
        model = Guest
        fields = (
            'number_of_party',
            'timeunit',
            'restaurant_id',
            'count',
        )